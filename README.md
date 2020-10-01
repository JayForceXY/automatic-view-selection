# automatic-view-selection

To generate candidate views using join as a similarity metric use 


python3 suggest_views.py [yes|no]  input_file.sql >> output_file.sql

yes : generates views with predicat 
no : generates views without predicat 


To generate candidate views using clustering to measure similarity use : 

python3 suggest_views_clustering_approach.py [yes|no] input_file.sql >> output_file.sql

yes: generates views with predicat 
no: generates views without predicat
