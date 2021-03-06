# ML 1D Convolutional NN for Proteins Solvent Accessibility Prediction

This project has been made for Machine Learning Corse at *University of Florence*.

The Problem
------
The prediction of proteins 3D structure's properties is one of the most popular and studied issue in bioinformatics and Machine Learning.<br>
Nowdays the most frequent approch is using a **Recurrent Neural Network**, like a Bidirectional-LSTM based Model (see [Linked articles](#the-linked-articles)
).<br>
Using a **Convolutional Neural Network** is a good compromise between *performance* and *execution time*.<br>
More details in the pdf [presentation](cnn_protein_solvent_accessibility_prediction.pdf).

The Idea
------
Even if the a RNN may capture more distant dependencies between the proteins amino acids, using a CNN will make sharply descend the execution time.
So the idea is using a CNN alone or combining it with a RNN (ispired from [1]), for capturing both local and gloabal dependencies between the features.

The Project
------
The project, realized with [**Keras**](https://github.com/keras-team/keras/), consists in a single [ipynb](https://ipython.org/ipython-doc/1/interactive/notebook.html) file: you can open it with [Google Colab](https://colab.research.google.com) or in you local notebook. Anyway i highly suggest to use a **GPU**...
There are also many data preprocessing classes and scripts:
1. *generate_sample.py*: Generate Random Samples from DSSP extracted from PDB (CullPDB folder).<br> **Note**: you have to put the PDB files in data/cullpdb/pdbs/<br>For example you can download the pdbs archive [CullPDB](http://www.princeton.edu/~jzthree/datasets/ICML2014/)
2. *prepare_dataset.py*: Script to generate train, validate and test set
3. *proteinStructureParser.py*: Parser of dataset metadata
4. *PDBParser.py*: PDB Parser class, used for conversion of PDB to DSSP to features
5. *Amino.py*,*Protein.py*: classes maybe utils for data analysis

The Dependencies
------
You will need:
- Python 3.x
- Keras
- Numpy
- CNN knowledge and time for the model training..

The Results
------
The CNN reached **85%** of accuracy, while the CNN-LSTM model obtained more than **89%** using CullPDB as dataset and training the model in 120 epochs, even if the second one appear to be yet improvable.

The linked articles
------
1. S.K.Snderby, O. Winther. [*Protein secondary structure prediction with long short
term memory networks*](https://arxiv.org/abs/1412.7828). arXiv preprint arXiv:1412.7828, 2014.
2. A. R. Johansen, S.K.Snderby, O. Winther,[*Protein and secondary structure
prediction with convolutions and vertical-bi-directional rnns*](https://arxiv.org/abs/1604.07176), DTU, 2016