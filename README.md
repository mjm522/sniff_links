# Script to download different files from a page

The script sl/sniff_links.py downloads all files from a page and saves it in a folder.

The script currently downloads .pdf files, more types can be added by modifying the line ```file_types``` in the main function. For example:```file_types=['.pdf', '.zip']```

### instructions

1. Run ```./install_dependencies.sh``` to install pip install httplib2, validators, bs4

2. Run ```python sl/sniff_links.py -l <specify the url to be sniffed>```

3. By default a folder downloaded_files will be created inside the parent folder sniff_links. 

4. This can be modified by passing additional argument like

```
python sl/sniff_links.py -l <specify the url to be sniffed> -d <download folder path>
```

