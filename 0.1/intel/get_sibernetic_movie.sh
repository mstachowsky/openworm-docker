Xvfb :44 -listen tcp -ac -screen 0 1920x1080x24+32 &
export DISPLAY=:44
cd $HOME/sibernetic
./Release/Sibernetic -f worm_crawl_half_resolution &
yes | ffmpeg -r 30 -f x11grab -draw_mouse 0 -s 1920x1080 -i :44 -filter:v "crop=1200:800:100:100" -c:v libvpx -quality realtime -cpu-used 0 -b:v 384k -qmin 10 -qmax 42 -maxrate 384k -bufsize 1000k -an $HOME/shared/sibernetic.webm
