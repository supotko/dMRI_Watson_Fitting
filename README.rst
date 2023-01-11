=========================
Waston Fitting Standalone
=========================

Installation
------------
To install the standalone Watson fitting, run the following commands in the root folder of the project:

.. code-block:: console

    cd build; cmake ..; sudo make install; cd ..; python setup.py build_ext --inplace

Alternative:

.. code-block:: console

    cd build; cmake ..; make; cd ..; python setup.py build_ext --inplace
    sudo cp build/libwatsonfit.so /usr/lib
    sudo cp watsonfit.h /usr/include/

Helper for a Clean Installation
-------------------------------

Miniconda:

.. code-block:: console

    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    chmod +x Miniconda3-latest-Linux-x86_64.sh
    ./Miniconda3-latest-Linux-x86_64.sh

Required Python libraries:

.. code-block:: console

    conda install numpy scipy matplotlib -y
    conda install -c conda-forge dipy fury pynrrd plyfile psutil nibabel vtk -y
    conda install -c anaconda cython -y
    pip install pyshtools

Required C/C++ libraries:

.. code-block:: console

    sudo apt install build-essential python3.8-dev cmake libcerf-dev -y

Installation of Ceres-Solver:

.. code-block:: console

    sudo apt-get install libgoogle-glog-dev libgflags-dev libatlas-base-dev libeigen3-dev libsuitesparse-dev -y
    wget http://ceres-solver.org/ceres-solver-2.1.0.tar.gz
    tar zxf ceres-solver-2.1.0.tar.gz
    mkdir ceres-bin
    cd ceres-bin
    cmake ../ceres-solver-2.1.0
    make -j3
    sudo make install
    cd ..

Installation of FSL, download file via https://fsl.fmrib.ox.ac.uk/fsl/fslwiki/FslInstallation:

.. code-block:: console

    python fslinstaller.py

Installation of MRtrix3:

.. code-block:: console

    sudo apt-get install git g++ python libeigen3-dev zlib1g-dev libqt5opengl5-dev libqt5svg5-dev libgl1-mesa-dev libfftw3-dev libtiff5-dev libpng-dev -y
    git clone https://github.com/MRtrix3/mrtrix3.git
    cd mrtrix3
    ./configure
    ./build
    ./set_path

Now head to step **Installation**.

Watson fitting scripts
----------------------

watson-fitting
~~~~~~~~~~~~~~

Performs a fitting of Watson distributions to fODFs that are given in a higher-order tensor format.

Examples:

.. code-block:: console
    
    python watson-fitting --i /path/to/fodf_and_wmvolume/ -ob /outputfolder/watson_backup.npz -o /outputfolder/watson_tracking_data.nrrd
    python watson-fitting --init given --initfile /path/to/fodf_peaks.nrrd --i /path/to/fodf_and_wmvolume -ob /outputfolder/watson_backup.npz -o /outputfolder/watson_tracking_data.nrrd -vvi /outputfolder/watson_vvi_cone_data.nrrd

Parameters to set:

* :code:`--i`: Inputfolder should contain:
                                - fodf.nrrd
                                    - 4D input file containing fODFs in masked higher-order tensor format (1+#fODF coefficients,x,y,z)
                                    - If the file is named differently, use the --infile argument
                                - wmvolume.nrrd
                                    - The white matter mask.
                                    - If the file is named differently, use the --wmvolume argument
* :code:`--infile`: 4D input file containing fODFs in masked higher-order tensor format (1+#fODF coefficients,x,y,z)
* :code:`--wmvolume`: White matter mask.
* :code:`-o`: 5D output file with the approximation result (5,r,x,y,z), the first axis contains in place 0 the kappa value, in place 1 the volume fraction and in the remaining places the unit direction.
* :code:`-op`: 5D output file with the approximation result without kappa (4,r,x,y,z), the first axis contains in place 0 the volume fraction and in the remaining places the unit direction.
* :code:`-ob`: Backup file with data to later generate any of the supported outputs with watson-backup-to-data.
* :code:`-of`: If filename is set, Watson parameters are used to generate fodf data.
* :code:`-ofn`: Only export one distribution per voxel, 0 for principal direction, 1 and 2 for 2nd and 3rd. Default None.
* :code:`-vvi`: If filename is set, r files are generated beginning with the given filename that contain data to visualize as cones with vvi.
* :code:`-r`: Rank. Default 3.
* :code:`--init`: How the fitting should be initialized, defaults to 'lowrank' for the lowrank fit by Schultz and Seidel, 2008. Alternative 'rand' for random init or 'given' for given values. Default 'lowrank'.
* :code:`--initfile`: Precomputed values e.g. from lowrank fit as 5D file (4,r,x,y,z), used if init argument is set to 'given'.
* :code:`--kapparange`: Range of initial kappa values to randomly sample from. Default '39.9,40'.
* :code:`--wmmin`: Minimum WM density to compute watson fitting. Default 0.3.
* :code:`--nospread`: If added, the fitting only fits the lowrank tensors without added Watson spread.
* :code:`--nooutliers`: If added, the fitting does not check for outliers.
* :code:`--verbose`: Default True.

watson-backup-to-data
~~~~~~~~~~~~~~~~~~~~~

Allows for multiple outputs, such as files for the tracking or for visualization with vvi, given the Watson fitting '.npz' file.

Examples:

.. code-block:: console
    
    python watson-backup-to-data --i /outputfolder/watson_backup.npz -o /outputfolder/watson_tracking_data.nrrd -of /outputfolder/watson_estimated_fodf.nrrd

Parameters to set:

* :code:`--i`: Backup file.
* :code:`-o`: 5D output file with the approximation result (5,r,x,y,z), the first axis contains in place 0 the kappa value, in place 1 the volume fraction and in the remaining places the unit direction.
* :code:`-op`: 5D output file with the approximation result without kappa (4,r,x,y,z), the first axis contains in place 0 the volume fraction and in the remaining places the unit direction.
* :code:`-ob`: Backup file with data to later generate any of the supported outputs.
* :code:`-of`: If filename is set, Watson parameters are used to generate fodf data.
* :code:`-ofn`: Only export one distribution per voxel, 0 for principal direction, 1 and 2 for 2nd and 3rd. Default None.
* :code:`-vvi`: If filename is set, r files are generated beginning with the given filename that contain data to visualize as cones with vvi.
* :code:`--verbose`: Default True.

watson-fodf-sh-generation
~~~~~~~~~~~~~~~~~~~~~~~~~

This script creates the sh fodf data needed for the fodf interpolation watson tracking.

Examples:

.. code-block:: console
    
    python watson-fodf-sh-generation --i /path/to/fodf/ -m /path/to/data.nii.gz -o /outfolder_sh/fodf.nrrd

Parameters to set:

* :code:`--i`: Inputfolder should contain:
                                - fodf.nrrd
                                    - 4D input file containing fODFs in masked higher-order tensor format (1+#fODF coefficients,x,y,z)
                                    - If the file is named differently, use the --infile argument
* :code:`--infile`: 4D input file containing fODFs in masked higher-order tensor format (1+#fODF coefficients,x,y,z)
* :code:`-m`: data.nii.gz corresponding to fodf.
* :code:`-o`: 4D output file containing fODFs in masked higher-order tensor format (#fodf coefficients,x,y,z).
* :code:`--verbose`: Default True.