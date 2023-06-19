@callback(
    Output('a1_taxonomy_sunburst', 'figure'),
    Output('results-container', 'children'),
    Input('taxonomy_level_slider', 'value'),
    Input('search-dropdown', 'value'),
    Input({'type': 'ta-button', 'index': 'n_clicks'}, 'n_clicks')
)
def update_sunburst_level(level=None, search_term=None, button_index=None):
    # ----------------------- STRUCTURE BUTTON -------------------------
    if button_index is not None:
        search_term = button_index
    
    
    # ------------------------------ SEARCH ----------------------------
    if search_term != None:
        if search_term.startswith('WP_'):
            # Search by accession
            df = df_netflax.copy()
            mask = (df['at_accession'].str.contains(search_term, case=False)) | (df['t_accession'].str.contains(search_term, case=False))
            filtered_df = df.loc[mask]

            last_ring = filtered_df[filtered_df['at_accession'] == search_term]['taxa'].values[0] \
                if len(filtered_df[filtered_df['at_accession'] == search_term]['taxa'].values) > 0 \
                else filtered_df[filtered_df['t_accession'] == search_term]['taxa'].values[0]

            df['color'] = wedge_non_highlight
            df.loc[df['taxa'] == last_ring, 'color'] = wedge_highlight

            fig = create_sunburst_figure(df, 'color', wedge_highlight)

            sunburst_fig = fig
            dataset = df_netflax[df_netflax.values == search_term]
            fig_antitoxin, fig_toxin = create_protein_logos(search_term)
            structure_data, styles, chain_sequence = visualising_protein(search_term)

            results_div = create_results_div(
                f'Search results for "{search_term}"',
                html.Div([
                    dbc.Row([
                        html.H5('Antitoxin'),
                        dcc.Graph(id='antitoxin-logo', figure=fig_antitoxin),
                    ], width=5),
                    dbc.Col(width=1),
                    dbc.Row([
                        html.H5('Toxin'),
                        dcc.Graph(id='toxin-logo', figure=fig_toxin),
                    ], width=5),
                    dbc.Row([
                        html.H5('Toxin-Antitoxin Structure'),
                        dashbio.Molecule3dViewer(
                            id='dashbio-default-molecule3d',
                            modelData=structure_data,
                            styles=styles
                        ),
                    ]),
                    dbc.Row([
                        dashbio.SequenceViewer(
                            id='dashbio-default-sequenceviewer',
                            sequence=chain_sequence,
                        ),
                    ]),
                ])
            )

            return sunburst_fig, results_div

        elif search_term.startswith('D') or search_term.startswith('M') or search_term.startswith('Panacea'):
            # Search by node
            df = df_netflax.copy()
            mask = (df['at_domain'].str.contains(search_term, case=False)) | (df['t_domain'].str.contains(search_term, case=False))
            filtered_df = df.loc[mask]

            # Get the last ring based on the taxa of the selected row
            last_ring = ""
            if len(filtered_df[filtered_df['at_domain'] == search_term]['taxa'].values) > 0:
                last_ring = filtered_df[filtered_df['at_domain'] == search_term]['taxa'].values[0]
            elif len(filtered_df[filtered_df['t_domain'] == search_term]['taxa'].values) > 0:
                last_ring = filtered_df[filtered_df['t_domain'] == search_term]['taxa'].values[0]

            # Set the color of all matching segments to lightblue
            df['color'] = wedge_non_highlight
            df.loc[df['taxa'] == last_ring, 'color'] = wedge_highlight

            fig = create_sunburst_figure(df, 'color', wedge_highlight)

            sunburst_fig = fig
            dataset = df_netflax[df_netflax.values == search_term]
            table = create_table(dataset)
            results_div = create_results_div(f'Node: "{search_term}"', table)

            return sunburst_fig, results_div

        else:
            # Search by taxonomy at any level
            df = df_netflax.copy()
            df['color'] = wedge_non_highlight

            if search_term in df['superkingdom'].values:
                level = 0
                df.loc[df['superkingdom'] == search_term, 'color'] = wedge_highlight
            elif search_term in df['phylum'].values:
                level = 1
                df.loc[df['phylum'] == search_term, 'color'] = wedge_highlight
            elif search_term in df['class'].values:
                level = 2
                df.loc[df['class'] == search_term, 'color'] = wedge_highlight
            elif search_term in df['order'].values:
                level = 3
                df.loc[df['order'] == search_term, 'color'] = wedge_highlight
            elif search_term in df['family'].values:
                level = 4
                df.loc[df['family'] == search_term, 'color'] = wedge_highlight
            elif search_term in df['genus'].values:
                level = 5
                df.loc[df['genus'] == search_term, 'color'] = wedge_highlight
            elif search_term in df['taxa'].values:
                level = 6
                df.loc[df['taxa'] == search_term, 'color'] = wedge_highlight
            else:
                print(f'{search_term} does not exist')

            fig = create_sunburst_figure(df, 'color', wedge_highlight)

            sunburst_fig = fig
            dataset = df_netflax[df_netflax.values == search_term]
            table = create_table(dataset)
            results_div = create_results_div(f'Node: "{search_term}"', table)

            return sunburst_fig, results_div

   # ------------------------------ SLIDER ----------------------------

    # Create a sunburst chart with the selected number of levels
    dataset = df_netflax
    if level is None:
        level = 3  # default value if level is not selected

    # Creating the plot    
    fig = sunburst_plot = px.sunburst(
        data_frame = dataset,
        path = paths[level],
        color = 'superkingdom',
        color_discrete_sequence = px.colors.qualitative.Pastel,
    )
    fig.update_traces(
        marker = dict(line = dict(color = page_background, width = 0.75)),
        hovertemplate='<b>%{label} </b> <br>Taxonomy: %{id}<br>Number of TAs: %{value}',
    )
    fig.update_layout(
        plot_bgcolor = transparent_background,
        paper_bgcolor = transparent_background)
    
    sunburst_fig = fig
    table = create_table(dataset)

    return sunburst_fig, html.Div(
            children=[
                dbc.Row([
                    html.H4(f'Search results for "{search_term}"'),
                    dbc.Row([
                        'InfoBox'
                    ]),
                    dbc.Row([
                        dbc.Col([

                        ]),
                        dbc.Col([

                        ])
                    ]),
                    dbc.Row([
                        "Selection data",
                        html.Hr(),
                        html.Div(id = 'molecule-info-container')
                    ]),
                    dbc.Row([
                        'Filtered NetFlax Table Results',
                        html.Div(
                            table,
                            className='table-container',
                            style={'overflowX': 'auto', 'overflowY': 'scroll', 'maxHeight': '400px'}
                        )
                    ]),
                ]),
            ]
        )  
 
