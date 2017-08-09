import ROOT
from ROOT import gSystem, TFile, TH1D, TCanvas, TGraph, TAxis, TF1
from array import array

print("Please eneter the relevant parameters of your Ramsey Cycle sweep: \n")
startFreq = float(raw_input('Starting Frequency of Ramsey Cycles: \n'))
endFreq = float(raw_input('Ending Frequency of Ramsey Cycles: \n'))
stepNum = int(raw_input('Number of Steps between Start and End Frequencies: \n'))

stepSize = (endFreq-startFreq)/stepNum

frequencies = []
meanSzend = []

for n in range(0,stepNum+1):

	currentFreq = startFreq + n*stepSize
	frequencies.append(currentFreq)

	f = TFile('Freq'+str(currentFreq)+'.root')
	t = f.Get('neutronend')
	hist = TH1D('hist', "", 400,-1,1)

	t.Draw("Szend>>hist", "stopID==-1")

	print("Mean Szend: ")
	print(hist.GetMean())
	meanSzend.append(hist.GetMean())

x = array("d", frequencies)
y = array("d", meanSzend)

#f1 = TF1("f1", "-.5 - .5*cos((100*(pi)+8)*(29.16469-x))",29.16, 29.17)

graph = TGraph(stepNum+1,x,y)
graph.SetTitle("Szend Of Ramsey Cycles in Frequency Range from "+str(startFreq)+" to "+str(endFreq))
graph.GetXaxis().SetTitle("BField Frequency")
graph.GetYaxis().SetTitle("Mean Szend")
canvas = TCanvas("canvas","canvas",700,500)
graph.Draw()
#f1.Draw("same")

raw_input("Press Enter to Finish")
