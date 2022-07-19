# Box Plots
This code presents the patient's treatment plan quality indicators (qi) as planned by Varian Eclipse. Each patient was planned 4 times: 3 with different Multi-Leaf Collimators (MLC) with leaf widths of 2.5mm, 5mm and 10mm; and the clinically accepted plan. There is currently data for two anatomical sites: Prostate and Lung.

## Requirements
For this code to work, you will need to provide a .csv file matching the format of the template provided. All volumes are in centimetres cubed [cc]

## Bugs
...

## Limitations
The patients have all been planned using VMAT, however due to technical constraints, the 10mm leaf width plans are done using a Millennium 120 MLC. This MLC has 5mm leaves through the centre 40 leaves and 10mm leaves for the outer 20. Targets small enough to fit in the outer leaves completely were planned using one side of the outer leaves. Targets with a max size of 20cm (in any dimension) were treated in halves with minimal overlap.

The clinically accepted prostate plans are done to 70Gy while the leaf width plans have a max dose of 60Gy. To make sure any comparisons are valid, PTV and CTV values are compared as a percetage of dose, while organs at risk are compared by asolute dose in volume.

## How It Works
### Site Box Plots (qualityIndicatorBoxPlots.py)
This code returns all box and whisker plots of the patient data for a given anatomical site. The box and whisker plot will show the qi's of all three MLC leaf widths.

To run, select an anatomical site and type it into line 5 where prompted. Run the code to generate the box and whisker plot which will appear in a folder marked "Boxplots".

### Site QI v Volume (QIvVolume.py)
This code returns a scatter plot of a qi against Volume [cc]. All three leaf widths will be on the same plot with a corresponding trendline.

To run, select an anatomical site and type it into line 5 where prompted. Run the code to generate the box and whisker plot which will appear in a folder marked "Volume".

### Approximation Comparison (IMRTvVMAT.py)
Due to technical constraints, a VMAT compromise was necessary for the 10mm leaf width treatment plans. The two competing options were between a 15 field IMRT or using VMAT with a small portion of the Millennium 120 MLC. There is a clear advantage in using VMAT over an IMRT approximation, however, if the target ever exceeds the limited treatment region, this comparison test will provide a baseline to determine whether or not we can confidently use the 15 IMRT approximation.

Run the code to generate the box and whisker plot which will appear in a folder marked "output_IMRTvVMAT". All comparisons will be for Prostate patients.
