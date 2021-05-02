#clean IMDb files
import re

Chinese_titles_dict = {}

Chinese_titles_id_regex = re.compile(r'(tt\d{7}).+\tcmn\t',re.X) #captures id if the title is in mandarin chinese
Id_regex = re.compile(r'(tt\d{7})')

#tconst	titleType	primaryTitle	originalTitle	isAdult	startYear	endYear	runtimeMinutes	genres  ###Header from Title_basics.txt
Basics_info_regex = re.compile(r'tt\d{7}\t(\w+)\t([^\t]+)\t([^\t]+)\t\d\t([^\t]+)\t([^\t]+)\t[^\t]+\t([^\t]+)\n')

#tconst	averageRating	numVotes
Ratings_info_regex = re.compile(r'tt\d{7}\t(\d\.\d)\t(\d+)\n')

with open('Title_akas.txt','r',encoding='utf8') as data_file:
    while True:
        line = data_file.readline() #reading line by line as loading in the whole file under with open.. too expensive on memory
        if line == '':
            break 
        Check_is_chinese = Chinese_titles_id_regex.search(line)
        if Check_is_chinese is not None:
            for i in range(1,5):
                if Check_is_chinese:
                    Chinese_id = Check_is_chinese.group(1)
                    Chinese_titles_dict[Chinese_id] = None  #kept as dictionary bc don't want multiples

print("Done parsing for Chinese movies")

Movie_sample = Chinese_titles_dict.keys()
Movie_sample_dict = {}

with open('Title_basics.txt','r',encoding='utf8') as data_file:
    while True:
        line = data_file.readline()
        if line == '':
            break
        Id = Id_regex.search(line)
        if Id is not None:
            if Id.group(1) is not None:
                Id = Id.group(1)
                if Id in Movie_sample:    
                    Basic_info = Basics_info_regex.search(line)
                    if Basic_info:
                        Basic_info = [Basic_info.group(1),Basic_info.group(2),Basic_info.group(3),Basic_info.group(4),Basic_info.group(5),Basic_info.group(6)]
                        Movie_sample_dict[Id] = Basic_info

print("Done writing Chinese movie info")

with open('Title_ratings.txt','r',encoding='utf8') as data_file:
    while True:
        line = data_file.readline()
        if line == '':
            break
        Id = Id_regex.search(line)
        if Id is not None:
            if Id.group(1) is not None:
                Id = Id.group(1)
                if Id in Movie_sample:
                    Ratings_info = Ratings_info_regex.search(line)
                    if Ratings_info:
                        Movie_sample_dict[Id].append(Ratings_info.group(1))
                        Movie_sample_dict[Id].append(Ratings_info.group(2))
print("Done rating Chinese movies")

Movie_sample_dict_str = str(Movie_sample_dict)
Pretty_dict_str = Movie_sample_dict_str.replace("{",'').replace("}",'').replace('"','').replace("'",'').replace(': [','\t').replace('], ','\n').replace(",",'\t').replace('\\N','N/A').replace('\\',' ').replace(']','')

with open('Chinese_titles_sample.txt','w',encoding = 'utf8') as wf:
    wf.write("tconst\ttitleType\tprimaryTitle\toriginalTitle\tstartYear\tendYear\tgenres\taverageRating\tnumVotes\n")
    wf.write(Pretty_dict_str)
print("Done!")
