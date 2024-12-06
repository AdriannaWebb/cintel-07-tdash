##########################
#Imports
##########################

# Import necessary libraries
import seaborn as sns # For creating visualizations
from faicons import icon_svg # For adding icons to the dashboard

from shiny import reactive # For reactivity and dynamic updates
from shiny.express import input, render, ui # Core PyShiny components
import palmerpenguins # For the penguins dataset
from pathlib import Path #for navigating to the styles.css 


##########################
#Load Data
##########################

# Load the Palmer Penguins dataset
df = palmerpenguins.load_penguins()

#############################
#Define the Shiney Express UI
#############################

# Set up the main UI layout with a title and fillable sidebar
ui.page_opts(
    title=ui.tags.div(
        "Penguins Characteristics Explorer", 
        style="font-weight: bold; font-size: 20px;"
    ),
    fillable=True
)
# Sidebar controls for filtering and navigation
with ui.sidebar(title="Filter controls"):
    # Slider to filter by penguin body mass
    ui.input_slider("mass", "Mass (g)", 2000, 6000, 6000)
    
    # Checkbox group to filter by penguin species
    ui.input_checkbox_group(
        "species",
        "Filter by Species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Adelie", "Gentoo", "Chinstrap"],
    )

    # Horizontal line for visual separation
    ui.hr()
    ui.h6("Source Links")

    # Links to helpful resources and source code
    ui.a(
        "GitHub Source",
        href="https://github.com/denisecase/cintel-07-tdash",
        target="_blank",
    )
    ui.a(
        "GitHub App",
        href="https://denisecase.github.io/cintel-07-tdash/",
        target="_blank",
    )
    ui.a(
        "GitHub Issues",
        href="https://github.com/denisecase/cintel-07-tdash/issues",
        target="_blank",
    )
    ui.a("PyShiny", href="https://shiny.posit.co/py/", target="_blank")
    ui.a(
        "Template: Basic Dashboard",
        href="https://shiny.posit.co/py/templates/dashboard/",
        target="_blank",
    )
    ui.a(
        "See also",
        href="https://github.com/denisecase/pyshiny-penguins-dashboard-express",
        target="_blank",
    )

# Main layout section with value boxes and summaries
with ui.layout_column_wrap(fill=False):
    # Display total number of penguins in the dataset
    with ui.value_box(showcase=ui.tags.div(icon_svg("earlybirds"), style="color: #43a5be;")):
        "Total Penguins In Dataset"
        @render.text
        def count():
            return filtered_df().shape[0] # Filtered dataset count

    # Display average bill length
    with ui.value_box(showcase=ui.tags.div(icon_svg("ruler-horizontal"), style="color: #43a5be;")):
        "Average Bill Length (mm)"

        @render.text
        def bill_length():
            # Calculate the mean bill length
            return f"{filtered_df()['bill_length_mm'].mean():.1f} mm"

    # Display average bill depth
    with ui.value_box(showcase=ui.tags.div(icon_svg("ruler-vertical"), style="color: #43a5be;")):
        "Average Bill Depth (mm)"

        @render.text
        def bill_depth():
            # Calculate the mean bill depth
            return f"{filtered_df()['bill_depth_mm'].mean():.1f} mm"

# Layout section for visualizations and dataset preview
with ui.layout_columns():
    # Scatter plot of bill length vs bill depth
    with ui.card(full_screen=True):
        ui.card_header("Bill Length vs. Bill Depth by Species")

        @render.plot
        def length_depth():
            # Scatter plot with seaborn
            return sns.scatterplot(
                data=filtered_df(),
                x="bill_length_mm",
                y="bill_depth_mm",
                hue="species",
            )

    # Data table preview of the penguin dataset
    with ui.card(full_screen=True):
        ui.card_header("Penguin Dataset Preview")

        @render.data_frame
        def summary_statistics():
            # Select columns to display in the data table
            cols = [
                "species",
                "island",
                "bill_length_mm",
                "bill_depth_mm",
                "body_mass_g",
            ]
            return render.DataGrid(filtered_df()[cols], filters=True)


#ui.include_css(app_dir / "styles.css")
ui.include_css(Path(__file__).parent / "styles.css")


##########################
#Define the reactive calc
##########################

# Reactive function to filter the dataset based on user inputs
@reactive.calc
def filtered_df():
    filt_df = df[df["species"].isin(input.species())]
    filt_df = filt_df.loc[filt_df["body_mass_g"] < input.mass()]
    return filt_df
