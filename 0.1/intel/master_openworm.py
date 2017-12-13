from __future__ import print_function
import errno
import matplotlib
matplotlib.use('Agg')
import shutil
from subprocess import call, Popen, PIPE
import os
import pwd
import shlex
import sys

OW_OUT_DIR = os.environ['OW_OUT_DIR']

def execute_with_realtime_output(command, directory, env=None):
    p = None
    try:
        p = Popen(shlex.split(command), stdout=PIPE, bufsize=1, cwd=directory, env=env)
        with p.stdout:
            for line in iter(p.stdout.readline, b''):
                print(line, end="")
        p.wait() # wait for the subprocess to exit
    except KeyboardInterrupt as e:
        print("Caught CTRL+C")
        if p:
            p.kill()
        raise e


sys.path.append(os.environ['C302_HOME']) 

try:
    os.system('xhost +')
except:
    print("Unexpected error: %s" % sys.exc_info()[0])


try:
    # dirty hack to fix an issue changing the output directory of Sibernetic
    os.system('ln -s %s %s' % (OW_OUT_DIR, os.path.join(os.environ['SIBERNETIC_HOME'], 'simulations')))
except:
    print("Unexpected error: %s" % sys.exc_info()[0])
    raise


try:
    if pwd.getpwuid(os.stat(OW_OUT_DIR).st_uid).pw_name != os.environ['USER']:
        os.system('sudo chown -R %s:%s %s' % (os.environ['USER'], os.environ['USER'], OW_OUT_DIR))
except:
    print("Unexpected error: %s" % sys.exc_info()[0])
    raise

#try:
#    os.system('sudo chown -R %s:%s %s' % ('ow', 'ow', os.environ['HOME']))
#except:
#    print("Unexpected error: %s" % sys.exc_info()[0])
#    raise


#try:
#    execute_with_realtime_output('make clean', os.environ['SIBERNETIC_HOME'])
#    execute_with_realtime_output('make all', os.environ['SIBERNETIC_HOME'])
#except KeyboardInterrupt as e:
#    sys.exit()



DEFAULTS = {'duration': 5.0, # 50 ms
            'dt': 0.005,
            'dtNrn': 0.05,
            'logstep': 100,
            'reference': 'FW',
            'c302params': 'C2',
            'verbose': False,
            'device': 'ALL',
            'configuration': 'worm_crawl_half_resolution',
            'noc302': False,
            'datareader': 'UpdatedSpreadsheetDataReader',
            'outDir': OW_OUT_DIR} 



print("****************************")
print("OpenWorm Master Script v.0.1")
print("****************************")
print("")
print("This script attempts to run a full pass through the OpenWorm scientific libraries.")
print("This depends on several other repositories being loaded to work and presumes it is running in a preloaded docker instance.")
print("It will report out where steps are missing.")
print("Eventually all the steps will be filled in.")
print("")

print("****************************")
print("Step 1: Rebuild c302 from the latest PyOpenWorm")
print("****************************")
print("not yet implemented.")


print("****************************")
print("Step 2: Execute the latest c302 simulation")
print("****************************")
"""
from runAndPlot import run_c302

orig_display_var = None
if os.environ.has_key('DISPLAY'):
    orig_display_var = os.environ['DISPLAY']
    del os.environ['DISPLAY'] # https://www.neuron.yale.edu/phpBB/viewtopic.php?f=6&t=1603







run_c302(DEFAULTS['reference'], 
         DEFAULTS['c302params'], 
         '', 
         DEFAULTS['duration'], 
         DEFAULTS['dt'], 
         'jNeuroML_NEURON', 
         data_reader=DEFAULTS['datareader'], 
         save=True, 
         show_plot_already=False,
         target_directory=os.path.join(os.environ['C302_HOME'], 'examples'),
         save_fig_to='tmp_images')

prev_dir = os.getcwd()
os.chdir(DEFAULTS['outDir'])
try:
    os.mkdir('c302_out')
except OSError as e:
    if e.errno != errno.EEXIST:
        raise

src_files = os.listdir(os.path.join(os.environ['C302_HOME'], 'examples', 'tmp_images'))
for file_name in src_files:
    full_file_name = os.path.join(os.environ['C302_HOME'], 'examples', 'tmp_images', file_name)
    print("COPY %s" % full_file_name)
    if (os.path.isfile(full_file_name)):
        shutil.copy2(full_file_name, 'c302_out')
shutil.rmtree(os.path.join(os.environ['C302_HOME'], 'examples', 'tmp_images'))
os.chdir(prev_dir)
if orig_display_var:
    os.environ['DISPLAY'] = orig_display_var
"""

print("****************************")
print("Step 3: Feed muscle activations into Sibernetic")
print("****************************")
print("not yet implemented.")


print("****************************")
print("Step 4: Run Sibernetic")
print("****************************")
"""try:
    os.chdir("/sibernetic")
    call(["apt-get", "install", "make"])
    call(["make", "clean"])
    call(["make", "all"])
    call(["Xvfb", ":1", "-screen", "0", "1024x768x16"])
    call(["export", "DISPLAY=:1.0"])
    call(["./Release/Sibernetic"])
except:
    print "Unexpected error:", sys.exc_info()[0]
    raise"""

try:
    command = """python sibernetic_c302.py 
                -duration %s 
                -dt %s 
                -dtNrn %s 
                -logstep %s 
                -device %s 
                -configuration %s 
                -reference %s 
                -c302params %s 
                -datareader %s 
                -outDir %s""" % \
                (DEFAULTS['duration'],
                DEFAULTS['dt'],
                DEFAULTS['dtNrn'], 
                DEFAULTS['logstep'], 
                DEFAULTS['device'], 
                DEFAULTS['configuration'], 
                DEFAULTS['reference'], 
                DEFAULTS['c302params'], 
                DEFAULTS['datareader'],
                'simulations') 
                #DEFAULTS['outDir'])
    execute_with_realtime_output(command, os.environ['SIBERNETIC_HOME'])
except KeyboardInterrupt as e:
    pass


all_subdirs = []
for dirpath, dirnames, filenames in os.walk('/home/ow/shared'):
    for directory in dirnames:
        if directory.startswith('C2_FW'):
            all_subdirs.append(os.path.join(dirpath, directory))

#all_subdirs = [d for d in os.listdir(OW_OUT_DIR) if (os.path.isdir(d) and d.startswith('%s_%s' % (DEFAULTS['c302params'], DEFAULTS['reference'])))]
#print(all_subdirs)
latest_subdir = max(all_subdirs, key=os.path.getmtime)


os.system('Xvfb :44 -listen tcp -ac -screen 0 1920x1080x24+32 &') # TODO: terminate xvfb after recording
os.system('export DISPLAY=:44')
os.system('tmux new-session -d -s SiberneticRecording "DISPLAY=:44 ffmpeg -r 30 -f x11grab -draw_mouse 0 -s 1920x1080 -i :44 -filter:v "crop=1200:800:100:100" -cpu-used 0 -b:v 384k -qmin 10 -qmax 42 -maxrate 384k -bufsize 1000k -an $HOME/shared/sibernetic_%s.mp4"' % os.path.split(latest_subdir)[-1])



command = './Release/Sibernetic -f %s -l_from lpath=%s' % (DEFAULTS['configuration'], latest_subdir)
#execute_with_realtime_output(command, os.environ['SIBERNETIC_HOME'])
execute_with_realtime_output(command, os.environ['SIBERNETIC_HOME'])

os.system('tmux send-keys -t SiberneticRecording q')

#ffmpeg_pids = os.system('pgrep ffmpeg')
#if isinstance(ffmpeg_pids, int):
#    ffmpeg_pids=[ffmpeg_pids]
#for ffmpeg_pid in ffmpeg_pids:
#    os.system('kill -9 %s' % ffmpeg_pid)








print("****************************")
print("Step 5: Extract skeleton from Sibernetic run for movement analysis")
print("****************************")
print("not yet implemented.")

print("****************************")
print("Step 6: Run movement analysis")
print("****************************")
print("not yet implemented.")
"""try:
    os.chdir("/movement_validation/tests")
    call(["nosetests", "--nocapture"])
except:
    print "Unexpected error:", sys.exc_info()[0]
    raise"""

print("****************************")
print("Step 7: Report on movement analysis fit to real worm videos")
print("****************************")
print("not yet implemented.")
