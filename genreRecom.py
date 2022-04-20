from datetime import datetime
import pandas as pd
import random
import numpy as np
import math


def mbtiGenreRecomendation(userGenre, userMbti):
    print( "[" + str( datetime.now() ) + "] Genre,Mbti Recomm started.." )
    mbtiRecommList = []
    genreRecommList = []

    ####################### mbti movie list return ###############################################
    ####################### mbti movie list return ###############################################
    ####################### mbti movie list return ###############################################

    file = open("data/mbti_genre.csv", "r", encoding='UTF8')
    file_reader = pd.read_csv(file)
    file_reader_Arr = file_reader.to_numpy()

    for i in range(len(file_reader_Arr)):
        if userMbti[0] == file_reader_Arr[i][0]:
            genre = file_reader_Arr[i][1]
            if "&" in genre:
                genrelist = genre.split("&")
                for genre in genrelist:
                    f = open("data/genre/genre_Top50/{0}_Top50".format(genre), "r", encoding='UTF8')
                    df = pd.read_csv(f)
                    ran10 = df.sample( int(10 / len(genrelist)))
                    for i in range(len(ran10)):
                        mbtiRecommList.append(ran10.iloc[i])
            else:
                f = open( "data/genre/genre_Top50/{0}_Top50".format(genre), "r", encoding='UTF8')
                df = pd.read_csv( f )
                ran10 = df.sample( 10 )
                for i in range( len( ran10 ) ):
                    mbtiRecommList.append( ran10.iloc[i] )

    random.shuffle(mbtiRecommList)

    ####################### genre movie list return ###############################################
    ####################### genre movie list return ###############################################
    ####################### genre movie list return ###############################################
    genreRecommListBase = []

    eachsample = math.ceil(10/len(userGenre))
    if len( userGenre ) > 1:
        cnt = 0
        for genre in userGenre:
            GenreList = []
            f = open("data/genre/genre_Top50/{0}_Top50".format(genre), "r", encoding='UTF8')
            df = pd.read_csv(f)
            for i in range(len(df)):
                GenreList.append(df.iloc[i])
            MooverCheckGenreList = MooverDel(mbtiRecommList, GenreList)
            GeoverCheckGenreList= GenreOverCheck(userGenre, MooverCheckGenreList)

            for i in range(eachsample):
                line = []
                genreRecommListBase.append(line)


            movieCnt = 0
            while cnt < len(genreRecommListBase):
                if GeoverCheckGenreList[movieCnt] not in genreRecommListBase:
                    genreRecommListBase[cnt] = GeoverCheckGenreList[movieCnt]
                    cnt += 1
                    movieCnt += 1
                else:
                    movieCnt += 1
        genreRecommList = genreRecommListBase
        print('len(genreRecommList)',len(genreRecommList))
    else:
        onegenre = userGenre[0]
        f = open("data/genre/genre_Top50/{0}_Top50".format(onegenre), "r", encoding='UTF8')
        df = pd.read_csv(f)
        totalGenreList = df.values.tolist()
        overchcList = MooverDel( mbtiRecommList, totalGenreList)
        genreRecommList = random.sample(overchcList, 10)
    print( "[" + str( datetime.now() ) + "] Genre,Mbti Recomm Finished.." )
    return mbtiRecommList, genreRecommList

########################################################################################################################
########################################################################################################################
########################################################################################################################
#mbti 중복 삭제
def MooverDel(mbtiRecommList, totalGenreList):
    overlapCnt = 0

    indexList = []
    for i in range( len( mbtiRecommList ) ):
        for j in range( len( totalGenreList ) ):
            if mbtiRecommList[i][0] == totalGenreList[j][0]:
                overlapCnt += 1
                indexList.append(j)
    print( "overlapCnt:", overlapCnt)
    for idx in sorted(indexList, reverse=True): #인덱스 고정(sorted) 상태로 내림차순(reverse=True)
        del totalGenreList[idx]
    return totalGenreList


def GenreOverCheck(userGenre, overCheckGenreList):
    uGenre = userGenre.copy()
    if '로맨스' in uGenre:
        for i in range(len(uGenre)):
            if '로맨스' in uGenre[i]:
                uGenre[i] = '멜로/로맨스'

    overchList = []

    for i in range(len(overCheckGenreList)):
        GeAllUnit = overCheckGenreList[i][3]
        GeAllUnitSpl = GeAllUnit.split(', ')
        GeAllUnitList = list(GeAllUnitSpl)
        overlab = set(uGenre) & set(GeAllUnitList)
        overchList.append(len(overlab))

    totalDfBase = pd.DataFrame(overCheckGenreList)
    totalDfBase.reset_index(inplace=True,drop=True)
    OverDf = pd.DataFrame(overchList, columns=['OverCnt'])
    totalDf = pd.concat([totalDfBase, OverDf], axis=1)
    finalDf = totalDf.sort_values(by=['OverCnt','meanScore','reviewCnt'], ascending=[False,False,False])
    finalList = finalDf.values.tolist()
    return finalList