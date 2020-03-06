from FWCore.ParameterSet.VarParsing import VarParsing
import FWCore.ParameterSet.Config as cms
import os, sys, json
from datetime import datetime

options = VarParsing("analysis")
options.register("address", "ailab01.fnal.gov", VarParsing.multiplicity.singleton, VarParsing.varType.string)
#options.register("address", "prp-gpu-1.t2.ucsd.edu", VarParsing.multiplicity.singleton, VarParsing.varType.string)
#options.register("inputfile", "step2.root", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("inputfile", "/data/t3home000/jkrupa/TTbarGSDR.root", VarParsing.multiplicity.singleton, VarParsing.varType.string)
#options.register("address", "18.4.112.82", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("port", 8001, VarParsing.multiplicity.singleton, VarParsing.varType.int)
options.register("timeout", 300, VarParsing.multiplicity.singleton, VarParsing.varType.int)
options.register("params", "", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("threads", 4, VarParsing.multiplicity.singleton, VarParsing.varType.int)
options.register("streams", 0,    VarParsing.multiplicity.singleton, VarParsing.varType.int)
options.register("batchsize", 16000,    VarParsing.multiplicity.singleton, VarParsing.varType.int)
options.register("modelname","facile", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("mode", "Async", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.register("hang", "", VarParsing.multiplicity.singleton, VarParsing.varType.string)
options.parseArguments()

if len(options.params)>0:
    with open(options.params,'r') as pfile:
        pdict = json.load(pfile)
    options.address = pdict["address"]
    options.port = int(pdict["port"])
    print("server = "+options.address+":"+str(options.port))

# check mode
allowed_modes = {
      
    "Async": "HcalPhase1Reconstructor_testAsync",
    "Sync": "HcalPhase1Reconstructor_testSync",
    "PseudoAsync": "HcalPhase1Reconstructor_testPseudoAsync",
}
if options.mode not in allowed_modes:
    raise ValueError("Unknown mode: "+options.mode)

from Configuration.StandardSequences.Eras import eras
process = cms.Process('HcalTest',eras.Run3)

#--------------------------------------------------------------------------------
# Import of standard configurations
#================================================================================
process.load('FWCore/MessageService/MessageLogger_cfi')
process.load('Configuration/StandardSequences/GeometryDB_cff')
process.load('Configuration/StandardSequences/MagneticField_38T_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('HLTrigger.Configuration.HLT_GRun_cff')
#process.GlobalTag.globaltag = cms.string('auto:phase1_2021_realistic')#100X_upgrade2018_realistic_v10')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2021_realistic', '')


process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(options.maxEvents) )
process.source = cms.Source("PoolSource",
    #fileNames = cms.untracked.vstring('file:../../Core/data/store_mc_RunIISpring18MiniAOD_BulkGravTohhTohbbhbb_narrow_M-2000_13TeV-madgraph_MINIAODSIM_100X_upgrade2018_realistic_v10-v1_30000_24A0230C-B530-E811-ADE3-14187741120B.root')
    fileNames = cms.untracked.vstring(['file:'+options.inputfile]*100),
    duplicateCheckMode = cms.untracked.string('noDuplicateCheck')
)

if len(options.inputFiles)>0: process.source.fileNames = options.inputFiles

###################### Hang #################################

if (options.hang != ""):
    l = options.hang.split(":")
    if not (len(l) == 2):
         raise Exception("Hang improperly formatted")
    hour = int(l[0])
    minute = int(l[1])
    if not (0 <= hour < 24):
        raise Exception("Hour not in proper range")
    if not (0 <= minute < 60):
        raise Exception("Minute not in proper range")
    print("Waiting until " + options.hang+".")
    hang = True

    while hang:
        nowHour = datetime.now().hour
        nowMinute = datetime.now().minute
        hang = not (hour <= nowHour and minute <= nowMinute)
    print("Signal received")

################### EDProducer ##############################
process.HcalProducer = cms.EDProducer("HcalPhase1Reconstructor_testSync",
    sipmQTSShift = cms.uint32(0),
    sipmQNTStoSum = cms.uint32(3),
    topN = cms.uint32(5),
    edmRecHitName = cms.InputTag("hbheprereco"),
    edmChanInfoName = cms.InputTag("hbheprereco"),                                           
    simHcalDigiName = cms.untracked.InputTag("simHcalDigis","HBHEQIE11DigiCollection"),
    Client = cms.PSet(
        ninput  = cms.uint32(15),
        noutput = cms.uint32(1),
        batchSize = cms.uint32(options.batchsize),
        address = cms.string(options.address),
        port = cms.uint32(options.port),
        timeout = cms.uint32(options.timeout),
        modelName = cms.string(options.modelname)
    )
)

# Let it run
#process.p = cms.Path(
#    process.HcalProducer
#)
process.hltHbhePhase1Reco = cms.EDProducer( "HBHEPhase1Reconstructor",
    tsFromDB = cms.bool( False ),
    setPulseShapeFlagsQIE8 = cms.bool( True ),
    use8ts = cms.bool( False ),
    digiLabelQIE11 = cms.InputTag("simHcalDigis","HBHEQIE11DigiCollection"),
    saveDroppedInfos = cms.bool( False ),
    setNoiseFlagsQIE8 = cms.bool( True ),
    saveEffectivePedestal = cms.bool( True ),
    digiLabelQIE8 = cms.InputTag( "hltHcalDigis" ),
    sipmQTSShift = cms.int32( 0 ),
    processQIE11 = cms.bool( True ),
    pulseShapeParametersQIE11 = cms.PSet(  ),
    algoConfigClass = cms.string( "" ),
    saveInfos = cms.bool( True ),
    flagParametersQIE11 = cms.PSet(  ),
    makeRecHits = cms.bool( True ),
    pulseShapeParametersQIE8 = cms.PSet( 
      UseDualFit = cms.bool( True ),
      LinearCut = cms.vdouble( -3.0, -0.054, -0.054 ),
      TriangleIgnoreSlow = cms.bool( False ),
      TS4TS5LowerThreshold = cms.vdouble( 100.0, 120.0, 160.0, 200.0, 300.0, 500.0 ),
      LinearThreshold = cms.vdouble( 20.0, 100.0, 100000.0 ),
      RightSlopeSmallCut = cms.vdouble( 1.08, 1.16, 1.16 ),
      TS4TS5UpperThreshold = cms.vdouble( 70.0, 90.0, 100.0, 400.0 ),
      TS3TS4ChargeThreshold = cms.double( 70.0 ),
      R45PlusOneRange = cms.double( 0.2 ),
      TS4TS5LowerCut = cms.vdouble( -1.0, -0.7, -0.5, -0.4, -0.3, 0.1 ),
      RightSlopeThreshold = cms.vdouble( 250.0, 400.0, 100000.0 ),
      TS3TS4UpperChargeThreshold = cms.double( 20.0 ),
      MinimumChargeThreshold = cms.double( 20.0 ),
      RightSlopeCut = cms.vdouble( 5.0, 4.15, 4.15 ),
      RMS8MaxThreshold = cms.vdouble( 20.0, 100.0, 100000.0 ),
      MinimumTS4TS5Threshold = cms.double( 100.0 ),
      LeftSlopeThreshold = cms.vdouble( 250.0, 500.0, 100000.0 ),
      TS5TS6ChargeThreshold = cms.double( 70.0 ),
      TrianglePeakTS = cms.uint32( 10000 ),
      TS5TS6UpperChargeThreshold = cms.double( 20.0 ),
      RightSlopeSmallThreshold = cms.vdouble( 150.0, 200.0, 100000.0 ),
      RMS8MaxCut = cms.vdouble( -13.5, -11.5, -11.5 ),
      TS4TS5ChargeThreshold = cms.double( 70.0 ),
      R45MinusOneRange = cms.double( 0.2 ),
      LeftSlopeCut = cms.vdouble( 5.0, 2.55, 2.55 ),
      TS4TS5UpperCut = cms.vdouble( 1.0, 0.8, 0.75, 0.72 )
    ),
    flagParametersQIE8 = cms.PSet( 
      hitEnergyMinimum = cms.double( 1.0 ),
      pulseShapeParameterSets = cms.VPSet( 
        cms.PSet(  pulseShapeParameters = cms.vdouble( 0.0, 100.0, -50.0, 0.0, -15.0, 0.15 )        ),
        cms.PSet(  pulseShapeParameters = cms.vdouble( 100.0, 2000.0, -50.0, 0.0, -5.0, 0.05 )        ),
        cms.PSet(  pulseShapeParameters = cms.vdouble( 2000.0, 1000000.0, -50.0, 0.0, 95.0, 0.0 )        ),
        cms.PSet(  pulseShapeParameters = cms.vdouble( -1000000.0, 1000000.0, 45.0, 0.1, 1000000.0, 0.0 )        )
      ),
      nominalPedestal = cms.double( 3.0 ),
      hitMultiplicityThreshold = cms.int32( 17 )
    ),
    setNegativeFlagsQIE8 = cms.bool( False ),
    setNegativeFlagsQIE11 = cms.bool( False ),
    processQIE8 = cms.bool( False ),
    algorithm = cms.PSet( 
      ts4Thresh = cms.double( 0.0 ),
      meanTime = cms.double( 0.0 ),
      nnlsThresh = cms.double( 1.0E-11 ),
      nMaxItersMin = cms.int32( 500 ),
      timeSigmaSiPM = cms.double( 2.5 ),
      applyTimeSlew = cms.bool( True ),
      timeSlewParsType = cms.int32( 3 ),
      ts4Max = cms.vdouble( 100.0, 20000.0, 30000.0 ),
      samplesToAdd = cms.int32( 2 ),
      deltaChiSqThresh = cms.double( 0.001 ),
      applyTimeConstraint = cms.bool( False ),
      timeSigmaHPD = cms.double( 5.0 ),
      useMahi = cms.bool( False ),
      correctForPhaseContainment = cms.bool( True ),
      respCorrM3 = cms.double( 1.0 ),
      pulseJitter = cms.double( 1.0 ),
      applyPedConstraint = cms.bool( False ),
      fitTimes = cms.int32( 1 ),
      nMaxItersNNLS = cms.int32( 500 ),
      applyTimeSlewM3 = cms.bool( True ),
      meanPed = cms.double( 0.0 ),
      ts4Min = cms.double( 0.0 ),
      applyPulseJitter = cms.bool( False ),
      useM2 = cms.bool( False ),
      timeMin = cms.double( -12.5 ),
      useM3 = cms.bool( False ),
      chiSqSwitch = cms.double( 15.0 ),
      dynamicPed = cms.bool( True ),
      tdcTimeShift = cms.double( 0.0 ),
      correctionPhaseNS = cms.double( 6.0 ),
      firstSampleShift = cms.int32( 0 ),
      activeBXs = cms.vint32( -1, 0, 1 ),
      ts4chi2 = cms.vdouble( 15.0, 15.0 ),
      timeMax = cms.double( 12.5 ),
      Class = cms.string( "SimpleHBHEPhase1Algo" )
    ),
    setLegacyFlagsQIE8 = cms.bool( False ),
    sipmQNTStoSum = cms.int32( 3 ),
    setPulseShapeFlagsQIE11 = cms.bool( False ),
    setLegacyFlagsQIE11 = cms.bool( False ),
    setNoiseFlagsQIE11 = cms.bool( False ),
    dropZSmarkedPassed = cms.bool( False ),
    recoParamsFromDB = cms.bool( True )
)

#process.hbheprereco.digiLabelQIE11 = cms.InputTag("simHcalUnsuppressedDigis","HBHEQIE11DigiCollection")
#process.hbheprereco.processQIE8 = cms.bool(False)
#process.hbheprereco.processQIE11 = cms.bool(True)
#process.hbheprereco.algorithm.useMahi = cms.bool(True)

process.digiPath = cms.Path(
    process.hcalDigis
)
process.recoPath = cms.Path(
    process.hbheprereco
)

#process.raw2digi_step = cms.Path(process.RawToDigi)
process.HcalProducer_step = cms.Path(process.hltHbhePhase1Reco) #process.hbheprereco)#process.HBHEPhase1Reconstructor)
process.endjob_step = cms.EndPath(process.endOfProcess)

process.MessageLogger.categories.append('FastReport')

#process.schedule = cms.Schedule(process.raw2digi_step,process.digiPath,process.recoPath,process.HcalProducer_step,process.endjob_step,process.endpath)
process.schedule = cms.Schedule(process.HcalProducer_step,process.endjob_step)
process.MessageLogger.cerr.FwkReport.reportEvery = 1
keep_msgs = ['TRTClient','HcalProducer']
for msg in keep_msgs:
    process.MessageLogger.categories.append(msg)
    setattr(process.MessageLogger.cerr,msg,
        cms.untracked.PSet(
            optionalPSet = cms.untracked.bool(True),
            limit = cms.untracked.int32(10000000),
        )
    )

if options.threads>0:
    if not hasattr(process,"options"):
        process.options = cms.untracked.PSet()
    process.options.numberOfThreads = cms.untracked.uint32(options.threads)
    process.options.numberOfStreams = cms.untracked.uint32(options.streams if options.streams>0 else 0)

from HLTrigger.Configuration.customizeHLTforMC import customizeHLTforMC 
process = customizeHLTforMC(process)


# instrument the menu with the FastTimerService
process.load( "HLTrigger.Timer.FastTimerService_cfi" )

# print a text summary at the end of the job
process.FastTimerService.printEventSummary        = False
process.FastTimerService.printRunSummary          = False
process.FastTimerService.printJobSummary          = True

