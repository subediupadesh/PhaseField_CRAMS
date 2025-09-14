# PhaseField CRAMS : Phase Field - Corrosion Resistant Additive Manufacturing Simulations
## Description of the Repository PhaseField_CRAMS
Primary Austenite (gamma) phase is more resitant to pitting or crevice corrosion as compared to ferrite (alpha) phase. 
Ni is assumed to be an Austenite stabilizer.
This repository consists of the data and codes related to phase field simulations of pseudo binary formulation for Duplex stainless steel to unravel the process-structure relationship in additively manufactured microstructures.
The pseudo-binary formulation for multicomponent steel is accomplished using pyMPEALab toolkit <a href="#ref1">[1]</a>. It is to be noted that differed processing parameters (P, vscan) can alter the growth kinetics and stability of gamma and alpha phases.
For example, the gamma phase is preferred more for AED = 5 J/mm2 as compared to 1.25 J/mm2. Such process parameter dependent differential structural evolution can be mechanistically modeled using phase field method. And, this knowledge could be utilized to programme the pitting resistance behavior of Duplex stainless steels.

<a name="ref1"></a>[1] pyMPEALab App [![multicomponentANN](https://img.shields.io/badge/pyMPEALab-streamlit-red)](https://pympealab.streamlit.app/)

The phase field simulations are performed in [MOOSE framework](https://mooseframework.inl.gov/). 
## Phase Field Modeling of Laser Processing
### Phase Evolution | Thermal History

<table>
  <tr>
    <td>
      <strong>High AED condition 5 J/mm²</strong><br>
      <img src="3_Simulation_Video_Animation/video_animations/high_AED/gif/highAED_Phase_evolve.gif" alt="Phase Evolution" width="400"/>
    </td>
    <td>
      <strong>High AED condition 5 J/mm²</strong><br>
      <img src="3_Simulation_Video_Animation/video_animations/high_AED/gif/highAED_T_dist.gif" alt="Temperature Distribution" width="400"/>
    </td>
  </tr>
  <tr>
    <td>
      <strong>Low AED condition 1.25 J/mm²</strong><br>
      <img src="3_Simulation_Video_Animation/video_animations/low_AED/gif/lowAED_Phase_evolve.gif" alt="Phase Evolution" width="400"/>
    </td>
    <td>
      <strong>Low AED condition 1.25 J/mm²</strong><br>
      <img src="3_Simulation_Video_Animation/video_animations/low_AED/gif/lowAED_T_dist.gif" alt="Temperature Distribution" width="400"/>
    </td>
  </tr>
</table>






The documentation of PhaseField_CRAMS is available in:


## Integrating experiments and phase field method through informatics  for tailored corrosion performance of additively manufactured steel microstructures.

[Mengistu Dagnaw](https://www.linkedin.com/in/),
[Sachin Poudel](https://www.linkedin.com/in/),
[Upadesh Subedi](https://www.linkedin.com/in/upadesh-s-0b321a15b/),
[Rubi Thapa](https://www.linkedin.com/in/),
[Łukasz Reimann](https://www.linkedin.com/in/),
[Augustine Nana Sekyi Appiah](https://www.linkedin.com/in/),
[Paweł M. Nuckowski](https://www.linkedin.com/in/),
[Mariusz Król](https://www.linkedin.com/in/),
[Zbigniew Brytan](https://www.linkedin.com/in/),
[Nele Moelans](https://www.linkedin.com/in/nele-moelans-57b1731/),
[Anil Kunwar](https://www.linkedin.com/in/anil-kunwar-9ba81653/)




