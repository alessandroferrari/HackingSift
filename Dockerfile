# Mattia Savardi nov, 17 2016
FROM	ubuntu:14.04
MAINTAINER Mattia Savardi <sava.met@gmail.com>

# Python setup
run	apt-get update 
run	sudo apt-get install -y python-numpy python-scipy python-matplotlib ipython ipython-notebook python-pandas python-sympy python-nose python-pip unzip

# Jupyter
run 	sudo pip install jupyter
run	jupyter notebook --generate-config
run	echo "c.NotebookApp.ip = '*'" >> ~/.jupyter/jupyter_notebook_config.py 
run	echo "c.NotebookApp.notebook_dir = u'/home/'" >> ~/.jupyter/jupyter_notebook_config.py 
run	echo "c.NotebookApp.open_browser = False" >> ~/.jupyter/jupyter_notebook_config.py 

# Opencv 2.4 setup
run	apt-get install -y -q wget curl
run	apt-get install -y -q build-essential
run	apt-get install -y -q cmake
#run	apt-get install -y -q python2.7 python2.7-dev 
#run	wget 'https://pypi.python.org/packages/2.7/s/setuptools/setuptools-0.6c11-py2.7.egg' && /bin/sh setuptools-0.6c11-py2.7.egg && rm -f setuptools-0.6c11-py2.7.egg
#run	curl 'https://raw.github.com/pypa/pip/master/contrib/get-pip.py' | python2.7
#run	pip install numpy
run	apt-get install -y -q libavformat-dev libavcodec-dev libavfilter-dev libswscale-dev
run	apt-get install -y -q libjpeg-dev libpng-dev libtiff-dev libjasper-dev zlib1g-dev libopenexr-dev libxine-dev libeigen3-dev libtbb-dev
run	sudo apt-get -qq install libopencv-dev build-essential checkinstall cmake pkg-config yasm libjpeg-dev libjasper-dev libavcodec-dev libavformat-dev libswscale-dev libdc1394-22-dev libxine-dev libgstreamer0.10-dev libgstreamer-plugins-base0.10-dev libv4l-dev python-dev python-numpy libtbb-dev libqt4-dev libgtk2.0-dev libmp3lame-dev libopencore-amrnb-dev libopencore-amrwb-dev libtheora-dev libvorbis-dev libxvidcore-dev x264 v4l-utils
run	wget https://github.com/opencv/opencv/archive/2.4.zip && unzip 2.4.zip && rm 2.4.zip 
run	cd opencv-2.4/ && mkdir release && cd release && cmake -D CMAKE_BUILD_TYPE=RELEASE -D CMAKE_INSTALL_PREFIX=/usr/local -D BUILD_PYTHON_SUPPORT=ON -D WITH_XINE=ON -D WITH_TBB=ON .. && make -j2 && make install && cd /
run	rm -rf opencv-2.4.7
run	export PYTHONPATH=/usr/local/python/2.7:$PYTHONPATH && sudo ldconfig && sudo ln /dev/null /dev/raw1394

expose 8888

cmd ipython notebook --port-retries=0 --port=8888 --no-browser --ip=*
