# Prostate Plots
This code presents the prostate patient's treatment plan quality indicators (qi) as planned by Varian Eclipse. Each patient was planned 4 times: 3 with different Multi-Leaf Collimators (MLC) with leaf widths of 2.5mm, 5mm and 10mm; and the clinically accepted plan.

## Requirements
For this code to work, you will need to provide a .csv file matching the format of the template provided. All volumes are in centimetres cubed [cc]

## Bugs
...

## Limitations
The patients have all been planned using 15 IMRT fields as an approximation for VMAT. The clincally planned values contain a mix of IMRT and VMAT.

The clinically accepted prostate plans are done to 70Gy while the leaf width plans have a max dose of 60Gy. To make sure any comparisons are valid, PTV and CTV values are compared as a percetage of dose, while organs at risk are compared by asolute dose in volume.

## How It Works
### Prostate Box Plots (qualityIndicatorBoxPlots.py)
This code returns a box and whisker plot of the prostate patient data. The box and whisker plot will show the qi's of all three MLC leaf widths with respect to the clinically accepted values and a horizontal line indicating where the difference is 0.

Select a qi from the QualIndi list and type it into line 5 where prompted. Run the code to generate the box and whisker plot. To compare absolute values (as opposed to difference between clinically planned values), comment out lines 37 & 38.

### Prostate QI v Volume ()

