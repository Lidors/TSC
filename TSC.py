#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 10:24:43 2020

@author: lidor
"""
import numpy as np
from phylib.stats import correlograms as CC
import joblib


def sortClu(filebase = None,shank = None,Nchannel = None):
    if any(x is None for x in [filebase,shank,Nchannel]):
        print('One of the following inputs is missins:\n filebase, shank, Nchannels ')
    else:
        

        clu, Nclu,res,spk = loadCRS(filebase  = filebase,shank = shank,Nchannel = Nchannel)

        X                 = CreatFeat(clu,res,spk)
        
        pathClu           = filebase+'.clu.'+shank
              
        x_prob            = writClu(X,clu,Nclu,pathClu)
     
        a     =np.sort(x_prob[x_prob>0.5])
        cutof =len(a)+1
        
        print('The clu cutof is:',cutof)






def loadCRS(filebase = None,shank = None,Nchannel = None):
   
    pathRes     = filebase+'.res.'+shank
    pathClu     = filebase+'.clu.'+shank
    pathSpk     = filebase+'.spk.'+shank
    nchannls    = Nchannel

    clu         = np.loadtxt(pathClu)
    Nclu        = clu[0]
    clu         = np.delete(clu,0)
    clu         = np.int16(clu)+1

    res         = np.loadtxt(pathRes)
    res         = np.int64(res)

    with open(pathSpk, 'rb') as fid:
        data_array = np.fromfile(fid, np.int16)
    spk =data_array.reshape([nchannls,32,-1],order='F')
    return (clu, Nclu,res,spk)




def CreatFeat(clu,res,spk):
    X     = []
    uni   = np.unique(clu)
    ccg   = CC(res, clu, cluster_ids = uni, sample_rate = 20000, bin_size = 20,
                         window_size = 20*60, symmetrize=True)
    for  num,i in enumerate(uni, start=0):
        i               = int(i)
        idx             = clu==i
        meanwf          = np.mean(spk[:,:,idx],axis=2)
        meanwf,ind      = trimSpk(meanwf)
        meanwf          = np.reshape(meanwf,8*32)
        SD              = np.std(spk[ind][:,:][:,:,idx],axis=2)
        SD              = np.reshape(SD,8*32)
        z               = ccg[num,num,:]
        maxZ            = np.max(z)
        if maxZ>0:
            z           = z/maxZ
#            z           = np.reshape(z,z.shape[2])
        else:
            z           = np.zeros(61)
        xtag        = np.concatenate((meanwf,SD,z))
        X           = np.concatenate((X,xtag))

    X    = np.reshape(X,(len(uni),-1))
    return(X)



def trimSpk(spk1):
    
    nChannels    = np.shape(spk1)
    
    if nChannels[0] ==8:
        spk     = spk1
        ind     = np.arange(0,8)
        
    elif nChannels[0] ==9:
        I       = np.argmax(np.abs(spk1[:,15]))
        if I<=4:
            ind   = np.arange(0,8)
            spk   = spk1[ind,:]
        else:
            ind   = np.arange(1,9)
            spk   = spk1[ind,:]
    elif nChannels[0] ==10:
        I       = np.argmax(np.abs(spk1[:,15]))
        if I<=4:
            ind   = np.arange(0,8)
            spk   = spk1[ind,:]
        else:
            ind   = np.arange(2,10)
            spk   = spk1[ind,:]
    elif nChannels[0] ==11:
        I       = np.argmax(np.abs(spk1[:,15]))
        if I<=4:
            ind   = np.arange(0,8)
            spk   = spk1[ind,:]
        elif I ==6:
            ind   = np.arange(2,10)
            spk   = spk1[ind,:]
        elif I>6:
            ind   = np.arange(3,11)
            spk   = spk1[ind,:]
             
    return(spk,ind)

def writClu(X,clu,Nclu,pathClu):
    model    = joblib.load('xg_001')
    x_prob   = model.predict_proba(X)
    x_prob   = x_prob[:,1]

    sortIdx  = np.argsort(x_prob,)
    sortIdx  = np.flip(sortIdx)
    cluN     = np.zeros(clu.shape)
    uni      = np.unique(clu)
    uni      = uni[sortIdx]
    

    for i in range(len(uni)):
        idx         = clu==uni[i]
        cluN[idx]   = i+2
    
    cluN   = np.insert(cluN,0,Nclu)
    cluN   = np.int16(cluN)
    np.savetxt(pathClu,cluN,delimiter='\n',fmt='%d')
    return(x_prob)


