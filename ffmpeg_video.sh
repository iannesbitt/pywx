#! /bin/bash

# Written by Ian Nesbitt, e4sciences LLC, 2016
# Requires ffmpeg (see https://github.com/ccrisan/motioneye/wiki/Install-On-Raspbian)

if [ -d "/home/pi/bin/pywx/img/arch/$(date +\%F)" ]; then
  cd /home/pi/bin/netcamscp/img/arch/$(date +\%F)

  # writes list of files, numbers each list item,
  # stores number and filename as vars, then renames files with numbering.
  # numbering is in %d format starting at 1.jpg
  ls | cat -n | while read n f; do mv "$f" "$n.jpg"; done
  # converts filenames with %d format to 30fps mp4 starting at 1.jpg
  ffmpeg -start_number 1 -r 30  -i \%d.jpg -c:v libx264 $(date +\%F).mp4

  # removes jpgs
  rm *.jpg
  # moves .mp4 up 1 level
  mv $(date +\%F).mp4 ../
  # removes current datestamped folder
  #cd ../; rm -r $(date +\%F)/

  cd ~/
fi
