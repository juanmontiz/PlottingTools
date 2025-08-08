# PlottingTools
## Some useful tools and functions for making different types of plots (box plots, violin plots, radar (spider), etc.).

- The box (violin) and swarm **palettes can be different**! In case they are the same, the box (violin) palette is set to be more translucid than the swarm so that the points can be clearly seen.
- Also, a custom palette can be provided.
- The arrays can have different numbers of elements.
- The code has to be executed twice for the **font_scale** to take effect (the ghosts in the machine...).
- If saveplot=True, the plot is saved in PNG, PDF, and SVG formats. Provide the filename **without extension**.
- Added an option to join points from joint distributions if they have the same number of elements (box plots, and box-swarm-halfviolin).

## Examples of box, violin plots, and box+swarm+halfviolin:
⚠️ Cannot connect pairs between 'label 1' and 'label 2': different lengths.

⚠️ Cannot connect pairs between 'label 2' and 'label 3': different lengths.
![box](https://github.com/user-attachments/assets/c6e32230-8a72-46c5-b8e5-c3e8c88af14d)
![violin](https://github.com/user-attachments/assets/ac34aca7-2eec-419c-bc9c-d9e1e72e842a)
![box+swarm+violin](https://github.com/user-attachments/assets/c16436ee-a029-4385-a131-615cb6aa51e8)
![radar (spider)](https://github.com/user-attachments/assets/032c0afd-6060-4137-916a-99d35b0592c5)
