# ms-celeb-extractor
Extraction tool to parse MS Celeb dataset

The MS Celeb Dataset https://github.com/EB-Dodo/C-MS-Celeb is a database of faces with 6,464,018
 images. 
 
 Due to some error, the original ![dataset is gone]https://github.com/EB-Dodo/C-MS-Celeb/issues/1 . 
 However, there is a torrent availble for use ![here] https://academictorrents.com/details/9e67eb7cc23c9417f39778a8e06cca5e26196a97/tech&hit=1&filelist=1 
 It contains a tsv file with the images encoded as base64 strings. 
 
 This extraction tool helps read through the tsv and place images of the same person in their respective folders. 
 
 The reasoning for this is: 
 
1. Most libraries have built in helper functions to parse such a structure, including ![pytorch] https://pytorch.org/docs/stable/torchvision/datasets.html#datasetfolder 
 ![keras/tensorflow] https://www.tensorflow.org/api_docs/python/tf/keras/preprocessing/image_dataset_from_directory 
2. Modern file systems hash their files, so if the path of the file is known, reading it is O(1) time 
3. Storing as the original jpeg files give a reduction from 95 GB to 57 GB 



## Usage and interface coming soon! 



## Contributing 
Feel free to add issues or pull requests

