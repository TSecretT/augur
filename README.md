<div align="center">

# Faugur
</div>

<div align="center">

Machine Learning algorithm to predict Faceit ongoing/upcoming matches.
</div>



  � | �
  ------------ | -------------
  ⏳ **Current Phase**| Parsing and preparing database
  📝**Total Matches Parsed** | ~6100
  🧭 **Parsing speed** | 0.66 s/match
 
 ### Features:
 * ***Python based project:*** every line of code is pure python.
 * ***Beginner friendly***: the logic behind this project is stupid simple. 
 * ***Mongo database***: flexible database lets us work with huge amount of data
 * ***Scalable***: due to it being DNN based, the model can be used on matches from other platforms.
 
 ### ToDo List:
 - [x] Match parsing
 - [x] Match sorting for future use
 - [x] Database communication
 - [x] Multiprocessing
 - [ ] Parsing several hubs at once 
 - [ ] Bypass Faceit Rate Limit 

## Notebook

### Phase 1

- 10000 matches (8000 train and 2000 test)
- Simple parsing logic with ~240 seconds per 100 matches.
- Each neuros is assigned to following key:
- - Average K/D Ratio
- - ...

10000 matches with only 16 inputs and 1 dense layers is not enough, after some tweaking the final prediction rate was **56%**
