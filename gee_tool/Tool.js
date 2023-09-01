// ------------------ DATA SETUP ------------------

var assets = {
    rf2018: ee.Image("projects/gee-tool/assets/classified_map_2018_fixedv8-cut-m2-fc-processed-6000"),
    table: ee.FeatureCollection("projects/gee-tool/assets/conservation_units_amazon_biome"),
    table2: ee.FeatureCollection("projects/gee-tool/assets/indigenous_area_amazon_biome"),
    mining: ee.Image("projects/gee-tool/assets/Mining"),
    pasture: ee.Image("projects/gee-tool/assets/pasture"),
    biome: ee.FeatureCollection("projects/gee-tool/assets/amazon_biome_border"),
    states: ee.FeatureCollection("projects/gee-tool/assets/states_amazon_biome"),
    fc: ee.Image("projects/gee-tool/assets/forest_cover_new"),
    gfc2024: ee.Image('projects/gee-tool/assets/year_1_pred'),
    gfc2025: ee.Image('projects/gee-tool/assets/cumulative-year2'),
    gfc2026: ee.Image('projects/gee-tool/assets/cumulative_3yr'),
    band1: ee.Image('projects/gee-tool/assets/interpret_merged_file_1'),
    band2: ee.Image('projects/gee-tool/assets/interpret_merged_file_2'),
    band3: ee.Image('projects/gee-tool/assets/merged_file_3_interpret'),
    carbonDensity: ee.ImageCollection("WCMC/biomass_carbon_density/v1_0")
  };
  
  // ------------------ UTILITY FUNCTIONS ------------------
  
  function extractCarbonDensity(imageCollection, biome, projection) {
    return imageCollection.first().clip(biome).resample('bilinear').reproject({
      crs: projection,
      scale: 6000
    });
  }
  
  
  function updatePredictionLayer(year) {
    var selectedImage;
    switch(year) {
      case 2024:
        selectedImage = assets.gfc2024;
        break;
      case 2025:
        selectedImage = assets.gfc2025;
        break;
      case 2026:
        selectedImage = assets.gfc2026;
        break;
    }
    
    var minVal = 0;
    var maxVal = 10500300;
    
    selectedImage = selectedImage.updateMask(selectedImage.gt(minVal).and(selectedImage.lte(maxVal)));
  
    if (main_layer !== null) {
      Map.remove(main_layer);
    }
  
    main_layer = ui.Map.Layer(selectedImage, {
      palette: ['#D0F5BE00', '#F0B86E', '#F94C10', '#C70039'],
      max: maxVal,
      min: minVal
    }, 'Predicted Deforestation');
    Map.layers().insert(1, main_layer);  // Insert after the ForestMasked layer
  }
  
  function updateInterpretabilityLayer(rank) {
    var selectedInterpretImage = null;
    
    if (rank === 1) {
      selectedInterpretImage = assets.band1;
    } else if (rank === 2) {
      selectedInterpretImage = assets.band2;
    } else if (rank === 3) {
      selectedInterpretImage = assets.band3;
    }
  
    // Remove the previous interpret layer
    if (interpret_main_layer !== null) {
      Map.remove(interpret_main_layer);
    }
    
    if (rank <= 3) {
  
      interpret_main_layer = ui.Map.Layer(selectedInterpretImage, {
        palette: ['#1f78b4', '#33a02c', '#e31a1c', '#ff7f00', '#6a3d9a', '#b15928', '#FFB6C1'],
        max: 7,
        min: 1
      }, 'interpret');
    
      // Always insert the interpret layer on top
      Map.layers().insert(2, interpret_main_layer);
      
    }
    
  }
  
  function handleMapClick(coords) {
      if (selectedImage) {
          var predictionValue = selectedImage.reduceRegion({
              reducer: ee.Reducer.mean(),
              geometry: ee.Geometry.Point(coords.lon, coords.lat),
              scale: 6000
          });
  
          var carbonDensityValue = carbonDensity.reduceRegion({
              reducer: ee.Reducer.mean(),
              geometry: ee.Geometry.Point(coords.lon, coords.lat),
              scale: 6000
          });
  
          predictionValue.evaluate(function(predictionResult) {
              carbonDensityValue.evaluate(function(carbonResult) {
                  updatePixelValueLabel(predictionResult.b1);
                  updateCarbonDensityLabel(carbonResult.carbon_tonnes_per_ha);
                  updateCarbonLostLabel(predictionResult.b1 * carbonResult.carbon_tonnes_per_ha);
              });
          });
      }
  }
  
  function removeLayerByName(layerName) {
    Map.layers().forEach(function(layer) {
      if (layer.getName() === layerName) {
        Map.remove(layer);
      }
    });
  }
  
  // Function to update the pixel value label
  // Outputs are rounded to 3sf, then to the nearest integer,
  // to avoid suggesting overly precise estimates
  function updatePixelValueLabel(value) {
    pixelValueLabel.setValue('Deforestation: ' + parseFloat((value/10000).toPrecision(3)).toFixed(0) + ' ha of 3600 ha');
  }
  
  function updateCarbonDensityLabel(value) {
    carbonDensityLabel.setValue('Carbon Stock: ' + parseFloat(value.toPrecision(3)).toFixed(0) + ' tonnes/ha');
  }
  
  function updateCarbonLostLabel(value) {
    carbonLostLabel.setValue('Potential Carbon Loss: ' + parseFloat((value/10000).toPrecision(3)).toFixed(0) + ' tonnes in 3600 ha pixel');
  }
  
  // ------------------ CONFIGURING STYLES ------------------
  // Base styles
  var baseStyles = {
      defaultPadding: '14px',
      defaultMargin: '10px',
      titleBackground: '#1A242F',
      contentBackground: '#ffffff',
      primaryFont: '17px',
      secondaryFont: '15px',
      boldFontWeight: 'bold',
      primaryColor: '#2980B9'
  };
  
  // Apply base styles
  var titleLabelStyle = {
      fontSize: baseStyles.primaryFont,
      fontWeight: baseStyles.boldFontWeight,
      padding: baseStyles.defaultPadding,
      color: baseStyles.primaryColor
  };
  
  var panelStyle = {
      width: '320px',
      padding: '8px',
      stretch: 'vertical',
      backgroundColor: baseStyles.contentBackground
  };
  
  var sliderLabelStyle = {
      fontWeight: baseStyles.boldFontWeight,
      fontSize: baseStyles.primaryFont,
      margin: '0 0 ' + baseStyles.defaultMargin + ' 0'
  };
  
  var sliderStyle = {
      stretch: 'horizontal',
      maxWidth: '500px',
      shown: true,
      margin: '0 ' + baseStyles.defaultMargin,
      padding: baseStyles.defaultPadding,
      backgroundColor: baseStyles.contentBackground,
      fontSize: baseStyles.primaryFont
  };
  
  var sliderRangeLabelStyle = {
      fontSize: '14px',
      margin: baseStyles.defaultMargin
  };
  
  var accordionHeaderStyle = {
      fontWeight: baseStyles.boldFontWeight,
      padding: baseStyles.defaultPadding,
      backgroundColor: baseStyles.titleBackground,
      stretch: 'horizontal',
      textAlign: 'left',
      color: '#ffffff'
  };
  
  var accordionPanelStyle = {
      stretch: 'horizontal',
      shown: false,
      padding: baseStyles.defaultPadding,
      backgroundColor: baseStyles.contentBackground
  };
  
  var accordionButtonStyle = {
      fontWeight: baseStyles.boldFontWeight,
      padding: baseStyles.defaultPadding,
      backgroundColor: baseStyles.contentBackground,
      color: baseStyles.primaryColor,
      fontSize: baseStyles.primaryFont,
      textAlign: 'left',
      shown: true,
      stretch: 'horizontal'
  };
  
  var sidebarStyle = {
      width: '360px',
      backgroundColor: baseStyles.contentBackground
  };
  
  var legendPanelStyle = {
      padding: baseStyles.defaultPadding,
      position: 'top-right'
  };
  
  var legendTitleStyle = {
      fontWeight: baseStyles.boldFontWeight,
      padding: baseStyles.defaultPadding,
      backgroundColor: baseStyles.titleBackground,
      fontSize: baseStyles.primaryFont,
      color: '#ffffff'
  };
  
  var legendStyles = {
      title: legendTitleStyle,
      contentPanel: {
          padding: baseStyles.defaultPadding,
          backgroundColor: baseStyles.contentBackground,
          margin: '0px'
      },
      floatingPanel: {
          backgroundColor: baseStyles.titleBackground,
          padding: '8px',
          margin: '0px',
          width: '290px'
      },
      colorBox: {
          width: '22px',
          height: '22px',
          margin: '0 ' + baseStyles.defaultMargin
      },
      label: {
          margin: '0 0 ' + baseStyles.defaultMargin + ' ' + baseStyles.defaultMargin
      }
  };
  
  
  var forestCoverStyle = {
    palette: ['#808080', '#A8DF8E'],  
    min: -1,
    max: 0
  };
  
  var predictionStyle = {
    palette: ['#D0F5BE00', '#F0B86E', '#F94C10', '#C70039'],
    max: 10500300,
    min: 0
  }
  
  // ------------------ CONFIGURING VARIABLES ------------------
  
  Map.setCenter(-62.2159, -3.4653, 5);
  
  var carbonDensity = extractCarbonDensity(
    assets.carbonDensity,
    assets.biome,
    assets.gfc2024.projection()
  );
  
  var forestmask = assets.fc.eq(0).or(assets.fc.eq(-1));
  var forestMasked = assets.fc.updateMask(forestmask);
  
  var selectedImage = assets.gfc2024; // Default selection
  var defaultYear = 2024;
  
  var deforestationColors = ['#D0F5BE', '#F0B86E', '#F94C10', '#C70039', '#808080']// '#A8DF8E'];
  var deforestationLabels = ['No Deforestation', '0 - 350 hectares', '351 - 700 hectares', '701 - 1050 hectares', 'Non-forest formations']// 'Forest Cover'];
  
  var interpret_main_layer = null;
  var interpretLabels = ['proximity to recent deforestation', ' forest edge density', 'mining', 'pasture', 'indigenous areas', 'protected areas', 'distance to roads'];
  var interpretColors = ['#1f78b4', '#33a02c', '#e31a1c', '#ff7f00', '#6a3d9a', '#b15928', '#FFB6C1'];
  
  // Functions to handle map click events
  Map.onClick(handleMapClick);
  
  // Load the forest cover map at the very bottom by default
  Map.layers().insert(0, ui.Map.Layer(forestMasked, forestCoverStyle, 'Forest Cover'));
  
  
  // Load the default prediction image on startup
  var main_layer = ui.Map.Layer(assets.gfc2024.updateMask(assets.gfc2024.gt(0).and(assets.gfc2024.lte(10500300)))
  , predictionStyle, 'Predicted Deforestation');
  Map.add(main_layer);
  
  // Define a list of overlays and their respective configurations
  var overlays = [
    {
      label: 'Indigenous areas',
      style: { color: '#DFCCFB', fillColor: '00000000', strokeWidth: 1.5, fillOpacity: 0, opacity: 1 },
      name: 'Indigenous areas',
      layerData: assets.table2,
      sourceLink: 'http://terrabrasilis.dpi.inpe.br/en/download-2/',
      sourceName: 'TerraBrasilis'
    },
    {
      label: 'Protected Areas',
      style: { color: '#5C4B99' },
      name: 'Protected Areas',
      layerData: assets.table,
      sourceLink: 'http://terrabrasilis.dpi.inpe.br/en/download-2/',
      sourceName: 'TerraBrasilis'
    },
    {
      label: 'Mining Areas',
      style: {
        palette: ['#982176']
      },
      name: 'Mining (Masked)',
      layerData: assets.mining,
      mask: function(data) {
        return data.updateMask(data.gte(0).and(data.lte(1)).not());
      },
      sourceLink: 'https://mapbiomas.org/en/download',
      sourceName: 'MapBiomas'
    },
    {
      label: 'Pasture',
      style: {
        palette: ['#FF6969']
      },
      name: 'Pasture (Masked)',
      layerData: assets.pasture,
      mask: function(data) {
        return data.updateMask(data.gte(0).and(data.lte(1)).not());
      },
      sourceLink: 'https://mapbiomas.org/en/download',
      sourceName: 'MapBiomas'
    },
    // {
    //   label: 'Biome',
    //   style: { color: '#000000', strokeWidth: 1.5, fillOpacity: 0, opacity: 1 },
    //   name: 'Biome',
    //   layerData: assets.biome,
    //   sourceLink: 'http://terrabrasilis.dpi.inpe.br/en/download-2/',
    //   sourceName: 'TerraBrasilis'
    // },
    {
      label: 'State Boundaries',
      style: { color: '#000000', strokeWidth: 1.5, fillOpacity: 0, opacity: 1 },
      name: 'States',
      layerData: assets.states,
      sourceLink: 'http://terrabrasilis.dpi.inpe.br/en/download-2/',
      sourceName: 'TerraBrasilis'
    },
    {
      label: 'Carbon Density',
      style: {
        palette: ['#F3FDE8', '#648040'],
        min: 0,
        max: 250
      },
      name: 'Carbon Density',
      layerData: carbonDensity,
      sourceLink: 'https://developers.google.com/earth-engine/datasets/catalog/WCMC_biomass_carbon_density_v1_0',
      sourceName: 'UNEP-WCMC'
    }
  ];
  
  // ------------------ UI SETUP ------------------
  
  var titleLabel = ui.Label('UN-REDD Deforestation Prediction App', titleLabelStyle);
  
  var selectionPanel = ui.Panel({
    layout: ui.Panel.Layout.flow('vertical'),
    style: panelStyle
  });
  
  function createRulerSlider(min, max, step, value, style, onChangeFunction) {
    var labels = [];
    for (var i = min; i <= max; i += step) {
      labels.push(ui.Label(i.toString(), {
          fontSize: '12px',
          backgroundColor: baseStyles.contentBackground  // Fix background color
      }));
    }
  
    var slider = ui.Slider({
      min: min,
      max: max,
      step: step,
      value: value,
      style: style,
      onChange: onChangeFunction
    });
  
    var panel = ui.Panel({
      widgets: [slider].concat(labels),
      layout: ui.Panel.Layout.flow('horizontal'),
      style: {
        backgroundColor: baseStyles.contentBackground
      }
    });
  
    return { panel: panel, slider: slider };
  }
  
  
  // Sliders
  var predictionComponents = createRulerSlider(2024, 2026, 1, 2024, sliderStyle, updatePredictionLayer);
  
  var interpretComponents = createRulerSlider(1, 3, 1, 1, sliderStyle, function(rank) {
    if (interpretCheckbox.getValue()) {
      updateInterpretabilityLayer(rank);
    }
  });
  
  var predictionSliderPanel = predictionComponents.panel;
  var predictionSlider = predictionComponents.slider;
  
  var interpretSliderPanel = interpretComponents.panel;
  var interpretSlider = interpretComponents.slider;
  
  
  
  var interpretCheckbox = ui.Checkbox('Click to see Feature Importance:', false);
  
  interpretCheckbox.onChange(function(checked) {
      interpretLegendFloating.style().set('shown', checked);
      
      if (checked) {
          var currentRank = interpretSlider.getValue();
          updateInterpretabilityLayer(currentRank);
      }
      else
      {
        updateInterpretabilityLayer(currentRank);
      }
  });
  
  // Separator
  var separator = ui.Label('', {backgroundColor: '#ccc', margin: '8px 0', height: '1px'});
  
  // Updated Panels with Grouping
  var predictionPanel = ui.Panel({
    widgets: [
      ui.Label('Deforestation Prediction', {
          fontWeight: 'bold',
          backgroundColor: baseStyles.contentBackground  // Fix background color
      }),
      predictionSliderPanel
    ],
    style: panelStyle,
    layout: ui.Panel.Layout.flow('vertical')
  });
  
  var interpretPanel = ui.Panel({
    widgets: [
      ui.Label('Feature Importance Interpretation', {
          fontWeight: 'bold',
          backgroundColor: baseStyles.contentBackground  // Fix background color
      }),
      interpretSliderPanel,
      interpretCheckbox
    ],
    style: panelStyle,
    layout: ui.Panel.Layout.flow('vertical')
  });
  
  // Add panels to selectionPanel
  selectionPanel.add(predictionPanel);
  selectionPanel.add(separator);
  selectionPanel.add(interpretPanel);
  
  var pixelValueLabel = ui.Label('Deforestation:', titleLabelStyle);
  var carbonDensityLabel = ui.Label('Carbon stock:', titleLabelStyle);
  var carbonLostLabel = ui.Label('Potential Carbon Lost:', titleLabelStyle);
  
  
  
  var checkedCount = 0;  // Maintain a count of checked checkboxes
  
  var overlayLegends = [];
  
  var checkboxes = overlays.map(function(overlay) {
      var checkbox = ui.Checkbox({ label: overlay.label, value: false });
  
      // Color box
      var colorBox = ui.Label({
          value: " ", 
          style: {
              backgroundColor: overlay.style.color || overlay.style.palette.slice(-1),
              padding: '8px',
              margin: '0 5px 0 0' // Right margin to space it from the label
          }
      });
  
      // Overlay name next to the color box
      var nameLabel = ui.Label(overlay.label, { fontWeight: 'bold' });
      var nameWithColor = ui.Panel({
          widgets: [colorBox, nameLabel],
          layout: ui.Panel.Layout.flow('horizontal')
      });
  
      // Source link (assuming UI framework supports hyperlinks)
    var sourceLinkLabel = ui.Label("Source: " + overlay.sourceName).setUrl(overlay.sourceLink);
  
      // Complete legend entry
      var legendPanel = ui.Panel({
          widgets: [nameWithColor, sourceLinkLabel],
          layout: ui.Panel.Layout.flow('vertical'),
          style: legendPanelStyle
      });
  
      // Hide the legend panel by default
      legendPanel.style().set('shown', false);
      overlayLegends.push(legendPanel);
  
      checkbox.onChange(function(checked) {
          var layerData = overlay.layerData;
  
          // Apply mask if defined for the overlay
          if (overlay.mask && layerData instanceof ee.Image) {
              layerData = overlay.mask(layerData);
          }
  
          if (checked) {
              Map.addLayer(layerData, overlay.style, overlay.name);
              legendPanel.style().set('shown', true);  // Show the legend
          } else {
              removeLayerByName(overlay.name);
              legendPanel.style().set('shown', false);  // Hide the legend
          }
          
          if (checked) {
              checkedCount += 1;
          } else {
              checkedCount -= 1;
          }
  
          // Decide to show or hide the overlay legend based on the checkedCount
          if (checkedCount > 0) {
              overlayLegendFloating.style().set('shown', true);
          } else {
              overlayLegendFloating.style().set('shown', false);
          }
      });
  
      return checkbox;
  });
  
  // Define a function to create an accordion-style panel
  function createAccordionPanel(title, widgets) {
      var panel = ui.Panel({
          widgets: widgets,
          layout: ui.Panel.Layout.flow('vertical'),
          style: accordionPanelStyle
      });
      
      var header = ui.Button({
          label: title,
          style: accordionButtonStyle  // This should now correctly style the button
      });
  
      header.onClick(function() {
          var isShown = panel.style().get('shown');
          panel.style().set('shown', !isShown);
      });
  
      return ui.Panel({
          widgets: [header, panel],
          layout: ui.Panel.Layout.flow('vertical')
      });
  }
  
  var collapseButton = ui.Button({
      label: '<<', // Or any icon/label that suggests collapsing
      onClick: function() {
          // Toggle the visibility of the sidebar
          var isShown = sidebar.style().get('shown');
          sidebar.style().set('shown', !isShown);
  
          // Change the label of the collapse button to indicate expand/collapse
          if (isShown) {
              collapseButton.setLabel('>>');
          } else {
              collapseButton.setLabel('<<');
          }
      }
  });
  
  var collapseButton = ui.Button({
      label: '<<', // Start with this since the sidebar will be shown initially
      onClick: function() {
          var isShown = sidebar.style().get('shown');
          
          // Toggle the visibility of the sidebar
          sidebar.style().set('shown', !isShown);
  
          // Adjust the label of the collapse button
          if (isShown) {
              collapseButton.setLabel('>>');
          } else {
              collapseButton.setLabel('<<');
          }
      }
  });
  
  collapseButton.style().set({
      position: 'top-left',
      padding: '10px'
  });
  
  // Create accordion panels for each section
  var dataViewPanel = createAccordionPanel('Data View', [
      predictionPanel,
      interpretPanel
  ]);
  
  var overlaysAccPanel = createAccordionPanel('Overlays', checkboxes);
  
  var analysisPanel = createAccordionPanel('Analysis (selected pixel)', [
      pixelValueLabel,
      carbonDensityLabel,
      carbonLostLabel,
  ]);
  
  // Content for Help accordion
  var helpContent = [
      ui.Label('How to use this app:'),
  
      ui.Label('- Data View:'),
      ui.Label('  This panel helps set up the base maps (interpretability and deforestation prediction). Use the "See feature importance" slider to switch between two modes. Two main sliders are present:'),
      ui.Label('  1. Predictions slider: Select predictions from 2024 to 2026.'),
      ui.Label('  2. Feature Importance slider: Choose the 1st, 2nd, or 3rd most important features.'),
  
      ui.Label('- Overlays:'),
      ui.Label('  This feature allows different layers to be displayed on top of the map, assisting in further analysis and interpretation of the base maps.'),
  
      ui.Label('- Analysis Tab:'),
      ui.Label('  This section provides information about specific locations. Click on the map, and the values in the tab will update to display carbon stock, deforestation prediction, and potential carbon loss for the selected location.'),
  
      ui.Label('- Legends:'),
      ui.Label('  Legends on the right provide color coding and sources for some of the overlays and base maps.'),
  
      ui.Label('- Navigation:'),
      ui.Label('  Both the side panel and legends are equipped with collapse buttons to optimize the viewing space.'),
  
      // Add more labels or widgets as needed to explain other functionalities of the app
  ];
  
  var helpAccordionPanel = createAccordionPanel('Help', helpContent);
  
  // Combine all accordion panels into a sidebar
  var sidebar = ui.Panel({
      widgets: [titleLabel, dataViewPanel, overlaysAccPanel, analysisPanel, helpAccordionPanel],
      layout: ui.Panel.Layout.flow('vertical'),
      style: sidebarStyle
  });
  
  // var sidebarContainer = ui.Panel({
  //     widgets: [collapseButton, sidebar],
  //     layout: ui.Panel.Layout.flow('vertical'),
  //     style: {
  //         position: 'top-left',
  //         padding: '10px'
  //     }
  // });
  
  
  // Add the sidebar to the map's UI
  ui.root.insert(0, sidebar);
  Map.add(collapseButton);
  
  // Add legends
  
  function createFloatingPanel(titleText, contentWidgets, position) {
      position = position || 'bottom-left';
  
      var contentPanel = ui.Panel({
          widgets: contentWidgets,
          layout: ui.Panel.Layout.flow('vertical'),
          style: {
            padding: legendStyles.contentPanel.padding,
            margin: legendStyles.contentPanel.margin,
            backgroundColor: baseStyles.contentBackground
          }
      });
  
      // Initially set the content to be hidden
      contentPanel.style().set('shown', true);
  
      // Use a button for the header to detect clicks
      var headerButton = ui.Button({
          label: titleText,
          style: {
              // General styles for the button appearance
              backgroundColor: legendStyles.floatingPanel.backgroundColor,
              border: 'none',
  
              // Text styling and alignment
              color: 'black',
              fontWeight: 'bold',
              textAlign: 'center',
              fontSize: '14px', // or any other size you prefer
              padding: '8px 12px', // vertical and horizontal padding
  
              // Spacing and size
              margin: legendStyles.floatingPanel.margin,
              width: legendStyles.floatingPanel.width,
          },
          onClick: function() {
              var currentState = contentPanel.style().get('shown');
              contentPanel.style().set('shown', !currentState);
          }
      });
  
      var panelStyle = {
          padding: '0',
          margin: '0',
          width: legendStyles.floatingPanel.width,
          position: position
      };
  
      return ui.Panel({
          widgets: [headerButton, contentPanel],
          layout: ui.Panel.Layout.flow('vertical'),
          style: panelStyle
      });
  }
  
  
  // Create Deforestation legend items
  var deforestationItemsPanel = ui.Panel({ layout: ui.Panel.Layout.flow('vertical', 'start') });
  deforestationColors.forEach(function(color, index) {
      var colorBoxStyle = {
          width: legendStyles.colorBox.width,
          height: legendStyles.colorBox.height,
          margin: legendStyles.colorBox.margin,
          backgroundColor: color
      };
      var colorBox = ui.Label({ style: colorBoxStyle });
      var colorBoxLabel = ui.Label(deforestationLabels[index], legendStyles.label);
      deforestationItemsPanel.add(ui.Panel({
          widgets: [colorBox, colorBoxLabel],
          layout: ui.Panel.Layout.flow('horizontal', 'start')
      }));
  });
  
  // Create Interpretability legend items
  var interpretItemsPanel = ui.Panel({ layout: ui.Panel.Layout.flow('vertical', 'start') });
  interpretColors.forEach(function(color, index) {
      var colorBoxStyle = {
          width: legendStyles.colorBox.width,
          height: legendStyles.colorBox.height,
          margin: legendStyles.colorBox.margin,
          backgroundColor: color
      };
      var colorBox = ui.Label({ style: colorBoxStyle });
      var colorBoxLabel = ui.Label(interpretLabels[index], legendStyles.label);
    
      var legendItemPanel = ui.Panel({
      widgets: [colorBox, colorBoxLabel],
      layout: ui.Panel.Layout.flow('horizontal', 'start'),
      style: {
          backgroundColor: baseStyles.contentBackground
      }
      });
      interpretItemsPanel.add(legendItemPanel);
  });
  
  
  
  // Construct the panels
  var interpretLegendFloating = createFloatingPanel('Interpretability Legend', [interpretItemsPanel], 'bottom-right');
  var overlayLegendFloating = createFloatingPanel('Overlay Legend', overlayLegends, 'middle-right');
  var deforestationLegendFloating = createFloatingPanel('Deforestation Legend', [deforestationItemsPanel], 'top-right');
  
  interpretLegendFloating.style().set('shown', false);
  overlayLegendFloating.style().set('shown', false);
  
  // Create a container panel for all legends
  var legendsContainer = ui.Panel({
      layout: ui.Panel.Layout.flow('vertical'),
      style: {
          position: 'bottom-right',
          width: legendStyles.floatingPanel.width + 20, // use the width of your existing legends
          backgroundColor: baseStyles.contentBackground // or 'transparent' if you don't want a background color
      }
  });
  
  // Add legends to the container
  legendsContainer.add(interpretLegendFloating);
  legendsContainer.add(overlayLegendFloating);
  legendsContainer.add(deforestationLegendFloating);
  
  // Add the container panel to the map
  var collapseLegendButton = ui.Button({
      label: '>>', // Or any icon/label that suggests collapsing
      onClick: function() {
          // Toggle the visibility of the sidebar
          var isShown = legendsContainer.style().get('shown');
          legendsContainer.style().set('shown', !isShown);
  
          // Change the label of the collapse button to indicate expand/collapse
          if (isShown) {
              collapseLegendButton.setLabel('<<');
          } else {
              collapseLegendButton.setLabel('>>');
          }
      }
  });
  
  collapseLegendButton.style().set({
      position: 'bottom-right',
      padding: '10px'
  });
  
  Map.add(collapseLegendButton);
  Map.add(legendsContainer);
  
  