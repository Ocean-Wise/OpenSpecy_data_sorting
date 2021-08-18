# OpenSpecy_data_sorting
Analysis based on OpenSpecy data

This repo uses heirarchical clustering (using scipy.cluster.heirarchy package) to sort spectra in OpenSpecy library into clusters. Clusters are formed by similarity criterion that if spectra have pearson correlation > 0.3, they are clustered together.

The files *ftir_library.csv* and *ftir_metadata.csv* are obtained from the OpenSpecy website current as of July 2021. The code data_arrange.py rearranges the spectra into a convenient dataframes *open_specy_ftir_library_INT.csv* and *open_specy_ftir_library_DERINT.csv* that contain the original and 1st derivative spectra, respectively.

Then, the Jupyter notebook nb_data_clustering.ipynb shows how heirarchical clustering is used to split the 636 spectra in the library as of July 2021 into 33 clusters based on the (pearson_r > 0.3) condition. The primary results of the clustering are illustrated using figures that show the clustering dendrogram (*dendrogram.png*) and mean/standard-deviation spectra for each cluster (*simplified_cluster_grid.png*)

The results are exported in 2 forms: a column *cluster_ix* is added to the original metadata table and is re-exported as the file *ftir_metadata_clusters.csv*, and a separate file *cluster_keys.csv* is created with a table of spectrum names corresponding to each cluster.

Up to this point, all processing is mechanical and follows python code as described above. However, there is a final step where **human judgement** is used to assign a simplified category name to each category based on knowledge of most commonly found polymers. These human generated simplified names are appended to the cluster keys table as a separate column *simplified_names* and exported as the file *cluster_keys_simplified.csv*
