from __future__ import print_function
from subprocess import call, Popen, PIPE
import os
import shlex
import sys

sys.path.append(os.environ['C302_HOME']) 



DEFAULTS = {'duration': 10.0,
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
            'outDir': os.path.join(os.environ['HOME'], 'shared')} 

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

print("****************************")
print("OpenWorm Master Script v.0.1")
print("****************************")
print("")
print("This script attempts to run a full pass through the OpenWorm scientific libraries.")
print("This depends on several other repositories being loaded to work and presumes it is running in a preloaded docker instance.")
print("It will report out where steps are missing.")
print("Eventually all the steps will be filled in.")
print("")

#print("****************************")
#print("Step 1: Rebuild c302 from the latest PyOpenWorm")
#print("****************************")



print("****************************")
print("Step 2: Execute the latest c302 simulation")
print("****************************")

from runAndPlot import run_c302
run_c302(DEFAULTS['reference'], 
         DEFAULTS['c302params'], 
         '', 
         DEFAULTS['duration'], 
         DEFAULTS['dt'], 
         'jNeuroML_NEURON', 
         data_reader=DEFAULTS['datareader'], 
         save=True, 
         show_plot_already=False, 
         save_fig_to=DEFAULTS['outDir'])


"""try:
    os.chdir(os.environ['C302_HOME'])
    call(["python", "c302_Full.py"])  # To regenerate the NeuroML & LEMS files
    call(["pynml", "examples/LEMS_c302_A_Full.xml"])   # Run a simulation with jNeuroML via [pyNeuroML](http://github.com/NeuroML/pyNeuroML)
except:
    print "Unexpected error:", sys.exc_info()[0]
    raise"""

"""print("****************************")
print("Step 3: Feed muscle activations into Sibernetic")
print("****************************")

try:
    os.chdir("/sibernetic/src")
    call(["wget", "https://github.com/pgleeson/Smoothed-Particle-Hydrodynamics/blob/master/src/main_sim.py"])
    call(["python", "main_sim.py"])
except:
    print "Unexpected error:", sys.exc_info()[0]
    raise"""

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
                -outDir %s""" % (DEFAULTS['duration'], DEFAULTS['dt'], DEFAULTS['dtNrn'], DEFAULTS['logstep'], DEFAULTS['device'], DEFAULTS['configuration'], DEFAULTS['reference'], DEFAULTS['c302params'], DEFAULTS['outDir'])
    execute_with_realtime_output(command, os.path.join(os.environ['HOME'], 'sibernetic'))
except KeyboardInterrupt as e:
    pass

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