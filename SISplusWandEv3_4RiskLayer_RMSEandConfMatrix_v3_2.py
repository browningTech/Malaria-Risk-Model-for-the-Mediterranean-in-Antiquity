##SCRIPT TO EVALUATE RELATIVE WEIGHTS OF MALARIA RISK LAYERS IN SELECTED, WITHHELD, and TOTAL AREAS - Percent Powers - 4 LAYERS  
import winsound
import arcpy
from arcpy import *
from arcpy.sa import *
from arcpy.da import *
##import time
arcpy.env.overwriteOutput = True
arcpy.env.extent = ("12 36 19 42")
arcpy.env.snapRaster = "F:\ArcGIS\Malaria Model\Italy\Calibration\SIS Layers Raw.gdb\SIS_DEMraw"
## >>>> - ENTER RANGES HERE in hundreds to make decimal percents - <<<<
ELrange = list(range(575,666,5))
TPrange = list(range(60,86,5))
PRrange = list(range(250,366,5))
TWIrange = list(range(5,26,5))
##GLOBAL VARIABLES
Area = "SIS"
SelectedArea = "W"
WithheldArea = "E"
Iteration = 0
CumPct = 0.00
resultstable = Area + "_Results"
resultstableSelected = resultstable + "_" + SelectedArea
resultstableWithheld = resultstable + "_" + WithheldArea
##CHECK IF EVALUATION TABLEs EXIST AND CREATE IF NOT
if arcpy.Exists(str(resultstable)) == True:
    print("Table is already present")
    ##FIND COMBINATIONS ALREADY RUN
    ValsList = []
    rcursor = SearchCursor(str(resultstable),['ELp','TPfp','PRp','TWIp'])
    for row in rcursor:
        entry = "el"+str(round(row[0],2))+"tp"+str(round(row[1],2))+'pr'+str(round(row[2],2))+'twi'+str(round(row[3],2))
        ValsList.append(entry)
    del rcursor
if arcpy.Exists(str(resultstable)) == False:
    arcpy.management.CreateTable(out_path=r"F:\ArcGIS\Malaria Model\Italy\Verification and Validation\Verification and Validation v3_2.gdb",out_name=resultstable,template=r"'F:\ArcGIS\Malaria Model\Italy\Verification and Validation\Verification and Validation v3_2.gdb\VandVresultstable'",config_keyword="",out_alias="")
    print("Table Created")
#### Selected Area
if arcpy.Exists(str(resultstableSelected)) == True:
    print("Selected Table is already present")
if arcpy.Exists(str(resultstableSelected)) == False:
    arcpy.management.CreateTable(out_path=r"F:\ArcGIS\Malaria Model\Italy\Verification and Validation\Verification and Validation v3_2.gdb",out_name=resultstableSelected,template=r"'F:\ArcGIS\Malaria Model\Italy\Verification and Validation\Verification and Validation v3_2.gdb\VandVresultstable'",config_keyword="",out_alias="")
    print("Selected Table Created")
#### Withheld Area
if arcpy.Exists(str(resultstableWithheld)) == True:
    print("Withheld Table is already present")
if arcpy.Exists(str(resultstableWithheld)) == False:
    arcpy.management.CreateTable(out_path=r"F:\ArcGIS\Malaria Model\Italy\Verification and Validation\Verification and Validation v3_2.gdb",out_name=resultstableWithheld,template=r"'F:\ArcGIS\Malaria Model\Italy\Verification and Validation\Verification and Validation v3_2.gdb\VandVresultstable'",config_keyword="",out_alias="")
    print("Withheld Table Created")
##INITIAL VARIABLE SETTINGS
if LowRMSE < 99.999:
    HighKappa = 0.1
    HighKappaSel = 0.1
    HighKappaWit = 0.1
    LowRMSE = 99.999
    LowRMSEW = 99.999
    LowRMSEE = 99.999
    Tor0RMSE = 99.999
    Tor1RMSE = 99.999
    Tor2RMSE = 99.999
    Tor3RMSE = 99.999
    AvgRMSE = 99.999
    STDRMSE = 99.999
    BestVals = "MxxxLxxxUxxSx"
    BestValsW = "MxxxLxxxUxxSx"
    BestValsE = "MxxxLxxxUxxSx"
EL = 0.0
PR = 0.0
TP = 0.0
TWI = 0.0
SLd = 0.0
##SET RASTERS##
baseline = Raster("Torelli03v3_buf100m")
Elev = Raster(str(Area) + "_DEM03")
TempPf = Raster(str(Area) + "_TP03")
##TempPv = Raster(str(Area) + "_TPv03")  ##Temp for P. vivax was eliminated as effectively contained within P. falciparum
Precip = Raster(str(Area) + "_PR03v3")
##Slope = Raster(str(Area) + "_Slope03") ##Slope was eliminated as non-contributing and contained in TWI 
TWI = Raster(str(Area) + "_TWI03")
##Initial Variables
##
EL_list = [round(x*0.001,3) for x in ELrange]
print(EL_list)
PR_list = [round(x*0.001,3) for x in PRrange]
print(PR_list)
TP_list = [round(x*0.001,3) for x in TPrange]
print(TP_list)
TWI_list = [round(x*0.001,3) for x in TWIrange]
print(TWI_list)
##Iteration Counter
ValsList = ()
PotInt = 0
for ELd in EL_list:
    CumPct = ELd
    for PRd in PR_list:
        CumPct = round((ELd + PRd),3)
        for TPd in TP_list:
            CumPct = round((ELd + PRd + TPd),3)
            if CumPct <= 1:
                for TWId in TWI_list:
                    CumPct = round((ELd + PRd + TPd + TWId),3)
                    ##print(CumPct)
                    if CumPct == 1:
                        PotInt = PotInt + 1
print("Process will POTENTIALLY take " + str(PotInt) + " Iterations")
for ELd in EL_list:
    ##print("EL pct: " + str(ELd))
    CumPct = ELd
    ##print("EL pct: " + str(ELd) + "Cumulative percent = " + str(CumPct))
    for PRd in PR_list:
        ##print("  PR pct: " + str(PRd))
        CumPct = round((ELd + PRd),3)
        ##RemPct = 1.0 - CumPct
        ##print("EL pct: " + str(ELd) + ", PR pct: " + str(PRd) + "; Cumulative percent = " + str(CumPct))
        for TPd in TP_list:
            CumPct = round((ELd + PRd + TPd),3)
            ##print("    TP pct: " + str(TPd) + "; cumulative pct = " +str(CumPct))
            if CumPct <= 1:
                ##print("    CumPct <= 1")
                ##print("EL pct: " + str(ELd) + ", PR pct: " + str(PRd) + ", TPf pct: " + str(TPd) + "; Cumulative percent = " + str(CumPct))
                for TWId in TWI_list:
                    CumPct = round((ELd + PRd + TPd + TWId),3)
                    ##print("      TWI pct: " + str(TWId) + "; cumulative pct = " +str(CumPct))
                    if CumPct == 1:
                        Vals = "el" + str(ELd) + "tp" + str(TPd) + "pr" + str(PRd) + "twi" + str(TWId)
                        if str(Vals) in ValsList: PotInt = PotInt - 1      
                        if str(Vals) in ValsList: continue
                        PrntVals = "EL pct: " + str(ELd) + ", TPf pct: " + str(TPd) + ", PR pct: " + str(PRd) + ", TWI pct: " + str(TWId)
                        fnVals = "el" + str(int(1000*ELd)) + "tp" + str(int(1000*TPd)) + "pr" + str(int(1000*PRd)) + "twi" + str(int(1000*TWId))
                        Iteration = Iteration +1
                        print("Iteration " + str(Iteration) + " of " + str(PotInt) + "; values: " + str(PrntVals) + "; Cumulative percent = " + str(CumPct))
                        rasname = Area + "_" + fnVals
                        savepath = r"F:\ArcGIS\Malaria Model\Italy\Verification and Validation\VandV_RescaledLayers_ConfMatrices v3_2.gdb"
                        saveras = savepath + "\\" + rasname
                        rasnameSave = 0
                        ## CALCULATIONS ## CALCULATIONS ## CALCULATIONS ## CALCULATIONS ## CALCULATIONS ## CALCULATIONS ## CALCULATIONS ##
                        ## - Full area Dif calculation
                        MalarRisk = ((Elev*ELd)+(TempPf*TPd)+(Precip*PRd)+(TWI*TWId))/CumPct
                        MalarRisk.save("MalarRisk") ##Save rescaled raster for use
                        Dif = Minus('Torelli03v3_buf100m',"MalarRisk") ##Establish difference by cell
                        Dif.save("Dif")  ##Save raster
                        ##print("Difference by cell calculated")
                        SqDif = Square("Dif")  ##Squared Difference by cell
                        SqDif.save("SqDif")  ##Save raster for use
                        ##
                        ##Create 'selecte' and 'withheld' error/difference rasters
                        ## "Selected" area !!!! SET extent values manually !!!!
                        with arcpy.EnvManager(extent='12 36 15 42 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'):                  
                            DifW = Minus('Torelli03v3_buf100m',"MalarRisk") ##Establish difference by cell from Torelli in West
                            DifW.save("DifW")  ##Save raster
                        ## "Withheld" area !!!! SET extent values manually !!!!
                        with arcpy.EnvManager(extent='15 36 19 42 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'):                  
                            DifE = Minus('Torelli03v3_buf100m',"MalarRisk") ##Establish difference by cell from Torelli in East
                            DifE.save("DifE")  ##Save raster 
                        print("Difference by cell calculated")
                        SqDifW = Square("DifW")  ##Squared Difference by cell
                        SqDifW.save("SqDifW")  ##Save raster for use
                        SqDifE = Square("DifE")  ##Squared Difference by cell
                        SqDifE.save("SqDifE")  ##Save raster for use
                        ##
                        ####  CONFUSION MATRIX  Production  ####
                        ##  Full Area Confusion Matrix
                        ConfMatrix = "ConfMtrx_" + Area + "_Iter" + str(fnVals)
                        saveCM = savepath + "\\" + ConfMatrix
                        ## Reclassify Model-produced Risk Layer
                        MALrcls = arcpy.sa.ReclassByTable(in_raster="MalarRisk",in_remap_table="Reclass2TorelliClass",from_value_field="From_value",to_value_field="To_value",output_value_field="Output_value",missing_values="NODATA")
                        print("Reclassed to Torelli classes")
                        MALrcls.save("MALrcls")
                        ## Create Assessment Points
                        print("Assessment Points . . .")
                        CreateAccuracyAssessmentPoints(in_class_data="MALrcls",out_points="AssPtsClass",target_field="CLASSIFIED",num_random_points=2000,sampling="STRATIFIED_RANDOM",polygon_dimension_field=None)
                        UpdateAccuracyAssessmentPoints(in_class_data="Torelli03v3_buf100m",in_points="AssPtsClass",out_points="AssmtPoints",target_field="GROUND_TRUTH",polygon_dimension_field=None,point_dimension_field=None)
                        ComputeConfusionMatrix(in_accuracy_assessment_points="AssmtPoints",out_confusion_matrix=str(saveCM))
                        arcpy.management.Delete( in_data="MALrcls",data_type="")
                        ##cursor to read Zonal Stats Table
                        CMcursor = SearchCursor(saveCM,["ClassValue","Total","U_Accuracy","Kappa"])
                        for row in CMcursor:
                            ##print(u'{0}, {1}, {2}'.format(row[0], row[1], row[2]))
                            if row[0] == "Total":
                                Tot = row[1]
                            if row[0] == "P_Accuracy":
                                AccAss = row[2]
                            if row[0] == "Kappa":
                                kappa = row[3]
                                print(str(Tot) + "  " + str(AccAss) + " " + str(kappa))
                        del CMcursor, row
                        print("Kappa = " + str(kappa))
                        if kappa >= HighKappa:
                            ##MalarRisk.save(saveras)
                            ##rasnameSave = 1
                            HighKappa = kappa
                            print("***NEW High Kappa = " + str(kappa) + " for values: " + Vals)
                            BestValsKappa = Vals
                        if kappa < HighKappa:
                            arcpy.management.Delete(in_data=str(ConfMatrix),data_type="")
                        ##
                        ##  "Selected" Area Confusion Matrix
                        ConfMatrixSel = "ConfMtrx_" + Area + SelectedArea + "_Iter" + str(fnVals)
                        saveCMSel = savepath + "\\" + ConfMatrixSel
                        ## Reclassify Model-produced Risk Layer
                        with arcpy.EnvManager(extent='12 36 15 42 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'):                  
                            MALrclsSel = arcpy.sa.ReclassByTable(in_raster="MalarRisk",in_remap_table="Reclass2TorelliClass",from_value_field="From_value",to_value_field="To_value",output_value_field="Output_value",missing_values="NODATA")
                            print("Reclassed to Torelli classes")
                            MALrclsSel.save("MALrclsSel")
                            ## Create Assessment Points
                            print("Assessment Points . . .")
                            CreateAccuracyAssessmentPoints(in_class_data="MALrclsSel",out_points="AssPtsClassSel",target_field="CLASSIFIED",num_random_points=2000,sampling="STRATIFIED_RANDOM",polygon_dimension_field=None)
                            UpdateAccuracyAssessmentPoints(in_class_data="Torelli03v3_buf100m",in_points="AssPtsClassSel",out_points="AssmtPointsSel",target_field="GROUND_TRUTH",polygon_dimension_field=None,point_dimension_field=None)
                            ComputeConfusionMatrix(in_accuracy_assessment_points="AssmtPointsSel",out_confusion_matrix=str(saveCMSel))
                            arcpy.management.Delete( in_data="MALrclsSel",data_type="")
                        ##cursor to read Zonal Stats Table
                        CMcursor = SearchCursor(saveCMSel,["ClassValue","Total","U_Accuracy","Kappa"])
                        for row in CMcursor:
                            ##print(u'{0}, {1}, {2}'.format(row[0], row[1], row[2]))
                            if row[0] == "Total":
                                TotSel = row[1]
                            if row[0] == "P_Accuracy":
                                AccAssSel = row[2]
                            if row[0] == "Kappa":
                                kappaSel = row[3]
                                print(str(TotSel) + "  " + str(AccAssSel) + " " + str(kappaSel))
                        del CMcursor, row
                        print("Kappa Selected = " + str(kappaSel))
                        if kappaSel >= HighKappaSel:
                            ##MalarRisk.save(saveras)
                            ##rasnameSave = 1
                            HighKappaSel = kappaSel
                            print("***NEW High Kappa = " + str(kappa) + " for values: " + Vals)
                            BestValsKappaSel = Vals
                        if kappaSel < HighKappaSel:
                            arcpy.management.Delete(in_data=str(ConfMatrixSel),data_type="")
                        ##
                        ##  "Withheld" Area Confusion Matrix
                        ConfMatrixWit = "ConfMtrx_" + Area + WithheldArea + "_Iter" + str(fnVals)
                        saveCMWit = savepath + "\\" + ConfMatrixWit
                        ## Reclassify Model-produced Risk Layer
                        with arcpy.EnvManager(extent='15 36 19 42 GEOGCS["GCS_WGS_1984",DATUM["D_WGS_1984",SPHEROID["WGS_1984",6378137.0,298.257223563]],PRIMEM["Greenwich",0.0],UNIT["Degree",0.0174532925199433]]'):                  
                            MALrclsWit = arcpy.sa.ReclassByTable(in_raster="MalarRisk",in_remap_table="Reclass2TorelliClass",from_value_field="From_value",to_value_field="To_value",output_value_field="Output_value",missing_values="NODATA")
                            print("Reclassed to Torelli classes")
                            MALrclsWit.save("MALrclsWit")
                            ## Create Assessment Points
                            print("Assessment Points . . .")
                            CreateAccuracyAssessmentPoints(in_class_data="MALrclsWit",out_points="AssPtsClassWit",target_field="CLASSIFIED",num_random_points=2000,sampling="STRATIFIED_RANDOM",polygon_dimension_field=None)
                            UpdateAccuracyAssessmentPoints(in_class_data="Torelli03v3_buf100m",in_points="AssPtsClassWit",out_points="AssmtPointsWit",target_field="GROUND_TRUTH",polygon_dimension_field=None,point_dimension_field=None)
                            ComputeConfusionMatrix(in_accuracy_assessment_points="AssmtPointsWit",out_confusion_matrix=str(saveCMWit))
                            arcpy.management.Delete( in_data="MALrclsWit",data_type="")
                        ##cursor to read Zonal Stats Table
                        CMcursor = SearchCursor(saveCMWit,["ClassValue","Total","U_Accuracy","Kappa"])
                        for row in CMcursor:
                            ##print(u'{0}, {1}, {2}'.format(row[0], row[1], row[2]))
                            if row[0] == "Total":
                                TotWit = row[1]
                            if row[0] == "P_Accuracy":
                                AccAssWit = row[2]
                            if row[0] == "Kappa":
                                kappaWit = row[3]
                                print(str(TotWit) + "  " + str(AccAssWit) + " " + str(kappaWit))
                        del CMcursor, row
                        print("Kappa Withheld = " + str(kappaWit))
                        if kappaWit >= HighKappaWit:
                            ##MalarRisk.save(saveras)
                            ##rasnameSave = 1
                            HighKappaSel = kappaSel
                            print("***NEW High Kappa = " + str(kappa) + " for values: " + Vals)
                            BestValsKappaWit = Vals
                        if kappaWit < HighKappaWit:
                            arcpy.management.Delete(in_data=str(ConfMatrixWit),data_type="")
                        ##
                        #### R M S E  Calculations and tabling  ####
                        print("Calculating RMSE")
                        tablename = "SqrErrorZS" ## generic tablename for SQUARED ERROR
                        ##  Zonal Stats FULL
                        ZonalStatisticsAsTable("Torelli03v3_buf100m","Value","SqDif",tablename,'DATA','MEAN') ##Get MEAN for Squared Error BY ZONE
                        AddField_management(tablename,'RMSE','FLOAT')  ##Add field for RMSE 
                        CalculateField_management(tablename,"RMSE",'math.sqrt(!MEAN!)',"PYTHON3") ##Calculate RMSE by Zone
                        Statistics_analysis(tablename,str(tablename)+"_STATS",[["RMSE","MEAN"],["RMSE","RANGE"],["RMSE","STD"]])##Get overall Avg, RANGE, and STD for zonal RMSE
                       ##  FOR SISW
                        ZonalStatisticsAsTable("Torelli03v3_buf100m","Value","SqDifW",str(tablename)+"W",'DATA','MEAN') ##Get MEAN for Squared Error BY ZONE
                        AddField_management(str(tablename) + "W",'RMSE','FLOAT')  ##Add field for RMSE 
                        CalculateField_management(str(tablename)+"W","RMSE",'math.sqrt(!MEAN!)',"PYTHON3") ##Calculate RMSE by Zone
                        Statistics_analysis(str(tablename)+"W",str(tablename)+"_STATSW",[["RMSE","MEAN"],["RMSE","RANGE"],["RMSE","STD"]])##Get overall Avg, RANGE, and STD for zonal RMSE
                        ##  FOR SISE
                        ZonalStatisticsAsTable("Torelli03v3_buf100m","Value","SqDifE",str(tablename)+"E",'DATA','MEAN') ##Get MEAN for Squared Error BY ZONE
                        AddField_management(str(tablename)+"E",'RMSE','FLOAT')  ##Add field for RMSE 
                        CalculateField_management(str(tablename)+"E","RMSE",'math.sqrt(!MEAN!)',"PYTHON3") ##Calculate RMSE by Zone
                        Statistics_analysis(str(tablename)+"E",str(tablename)+"_STATSE",[["RMSE","MEAN"],["RMSE","RANGE"],["RMSE","STD"]])##Get overall Avg, RANGE, and STD for zonal RMSE
                        ##get RMSE for each zone for adding to overall results by values table
                        ##cursor to read Zonal Stats Table 
                        ZScursor = SearchCursor(tablename,["Value","RMSE"])
                        for row in ZScursor:
                            if row[0] == 0:
                                Tor0RMSE = row[1]
                            if row[0] == 1:
                                Tor1RMSE = row[1]
                            if row[0] == 2:
                                Tor2RMSE = row[1]
                            if row[0] == 3:
                                Tor3RMSE = row[1]
                            print("Zone {}: RMSE = {}".format(row[0], row[1]))
                        del ZScursor
                        acursor = SearchCursor(str(tablename)+"_STATS",['MEAN_RMSE','STD_RMSE'], None)  ##Cursor for STATS table
                        for row in acursor:
                            AvgRMSE = row[0]
                            STDRMSE = row[1]
                            print("Average RMSE for all zones = {}".format(row[0]))
                            if AvgRMSE < LowRMSE:
                                LowRMSE = AvgRMSE
                                print("***NEW low RMSE = " + str(LowRMSE) + " for values: " + Vals)
                                BestVals = Vals
                            else:
                                print("BestVals still: " + BestVals + "; deleting lousy raster and table...")
                        del acursor
                        ## Selected
                        ##cursor to read Zonal Stats Table WWWWWW
                        ZScursorW = SearchCursor(str(tablename)+"W",["Value","RMSE"])
                        for row in ZScursorW:
                            if row[0] == 0:
                                Tor0RMSEW = row[1]
                            if row[0] == 1:
                                Tor1RMSEW = row[1]
                            if row[0] == 2:
                                Tor2RMSEW = row[1]
                            if row[0] == 3:
                                Tor3RMSEW = row[1]
                            print("Zone {}: RMSE = {}".format(row[0], row[1]))
                        del ZScursorW
                        acursorW = SearchCursor(str(tablename)+"_STATSW",['MEAN_RMSE','STD_RMSE'], None)  ##Cursor for STATS table
                        for row in acursorW:
                            AvgRMSEW = row[0]
                            STDRMSEW = row[1]
                            print("Average RMSE for all WEST zones = {}".format(row[0]))
                            if AvgRMSEW < LowRMSEW:
                                LowRMSEW = AvgRMSEW
                                print("***NEW low RMSE WEST = " + str(LowRMSEW) + " for values: " + Vals)
                                BestValsW = Vals
                            else:
                                print("BestVals WEST still: " + BestValsW + "; deleting lousy raster and table...")
                                ##time.sleep(5)  ##sleep time for deleting old files in earlier version; no longer needed???
                        del acursorW
                        ## Withheld
                        ##cursor to read Zonal Stats Table EEEEEE
                        ZScursorE = SearchCursor(str(tablename)+"E",["Value","RMSE"])
                        for row in ZScursorE:
                            if row[0] == 0:
                                Tor0RMSEE = row[1]
                            if row[0] == 1:
                                Tor1RMSEE = row[1]
                            if row[0] == 2:
                                Tor2RMSEE = row[1]
                            if row[0] == 3:
                                Tor3RMSEE = row[1]
                            print("Zone {}: RMSE = {}".format(row[0], row[1]))
                        del ZScursorE
                        acursorE = SearchCursor(str(tablename)+"_STATSE",['MEAN_RMSE','STD_RMSE'], None)  ##Cursor for STATS table
                        for row in acursorE:
                            AvgRMSEE = row[0]
                            STDRMSEE = row[1]
                            print("Average RMSE for all EAST zones = {}".format(row[0]))
                            if AvgRMSEE < LowRMSEE:
                                LowRMSEE = AvgRMSEE
                                print("***NEW low RMSE EAST = " + str(LowRMSEE) + " for values: " + Vals)
                                BestValsE = Vals
                            else:
                                print("BestVals EAST still: " + BestValsE)
                        del acursorE
                        ##
                        ##INSERT CURSOR STUFF . . . NOTE: ESTABLISH TABLES IF NOT ALREADY EXISTING BEFORE RUNNING SCRIPT!!
                        VarFields = ['ELp','TPfp','PRp','TWIp','Totalp','Tor0RMSE','Tor1RMSE','Tor2RMSE','Tor3RMSE','STDRMSE','AVGRMSE','Kappa','AccAss'] ##ADD ALL FIELDS HERE
                        tcursor = InsertCursor(resultstable,VarFields)
                        tcursor.insertRow((ELd,TPd,PRd,TWId,CumPct,Tor0RMSE,Tor1RMSE,Tor2RMSE,Tor3RMSE,STDRMSE,AvgRMSE,kappa,AccAss))
                        del tcursor
                        ##INSERT CURSOR STUFF . . . NOTE: ESTABLISH TABLES IF NOT ALREADY EXISTING BEFORE RUNNING SCRIPT!!
                        ## SISW 
                        VarFields = ['ELp','TPfp','PRp','TWIp','Totalp','Tor0RMSE','Tor1RMSE','Tor2RMSE','Tor3RMSE','STDRMSE','AVGRMSE','Kappa','AccAss'] ##ADD ALL FIELDS HERE
                        tcursorW = InsertCursor(str(resultstable)+"_W",VarFields)
                        tcursorW.insertRow((ELd,TPd,PRd,TWId,CumPct,Tor0RMSEW,Tor1RMSEW,Tor2RMSEW,Tor3RMSEW,STDRMSEW,AvgRMSEW,kappaSel,AccAssSel))
                        del tcursorW
                        ## SISE 
                        VarFields = ['ELp','TPfp','PRp','TWIp','Totalp','Tor0RMSE','Tor1RMSE','Tor2RMSE','Tor3RMSE','STDRMSE','AVGRMSE','Kappa','AccAss'] ##ADD ALL FIELDS HERE
                        tcursorE = InsertCursor(str(resultstable)+"_E",VarFields)
                        tcursorE.insertRow((ELd,TPd,PRd,TWId,CumPct,Tor0RMSEE,Tor1RMSEE,Tor2RMSEE,Tor3RMSEE,STDRMSEE,AvgRMSEE,kappaWit,AccAssWit))
                        del tcursorE
                        print("_________________")
                    ##else:
            ## End 4-TWI##
        ##End 3-TP##
    ##End 2-PR##
##End 1-EL##
duration = 1000  # milliseconds
freq = 440  # Hz
winsound.Beep(freq, duration)
##SEND EMAIL/TEXT
import smtplib, ssl
gmail_user = 'browningstep@gmail.com'
gmail_password = 'mqorpxmrknechecv'
##
message = """\
Subject:  ArcGIS Reports: It Is Finished!

 Done!"""

port = 465
sent_from = 'Python script'
to = '6013074159@txt.att.net'
##subject = 'From: ArcGIS'
##body = 'It is finished.'
email_text = "Done!"
context = ssl.create_default_context()
##
with smtplib.SMTP_SSL('smtp.gmail.com', port, context=context) as server:
    server.login(gmail_user, gmail_password)
    ##print("Connection Status: Logged in")
    server.sendmail(sent_from, to, message)
##CLEANUP
Delete_management(MalarRisk)
Delete_management(Dif)
Delete_management(SqDif)
Delete_management(DifW)
Delete_management(SqDifW)
Delete_management(DifE)
Delete_management(SqDifE)
##Delete_management(Malrcls)
##Delete_management(MalrclsSel)
##Delete_management(MalrclsWit)
##Delete_management(SqrErrorZS)
##Delete_management(SqrErrorZS_STATS)
print("Best values WEST are: " + BestValsW + " = RMSE: " + str(LowRMSEW))
print("Best values EAST are: " + BestValsE + " = RMSE: " + str(LowRMSEE))
print("Best values are: " + BestVals + " = RMSE: " + str(LowRMSE))
print("DONE!")
