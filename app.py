map.on(L.Draw.Event.CREATED, function(e){
    var layer = e.layer;
    var type = e.layerType;
    var label = "";

    // Розрахунок площі ТІЛЬКИ в км²
    if (type === 'rectangle' || type === 'polygon') {
        var areaM2 = L.GeometryUtil.geodesicArea(layer.getLatLngs()[0]);
        var areaKm2 = (areaM2 / 1000000).toFixed(2); // Переводимо м² у км²
        label = "S: " + areaKm2 + " км²";
    }
    
    // Розрахунок радіуса (залишаємо метри/кілометри для зручності)
    if (type === 'circle') {
        var radius = layer.getRadius();
        label = "R: " + (radius >= 1000 ? (radius/1000).toFixed(2) + ' км' : radius.toFixed(0) + ' м');
    }

    if (type === 'circlemarker') {
        layer.setStyle(solidYellowStyle);
    } else if (layer.setStyle) {
        layer.setStyle(yellowStyle);
    }
    
    drawnItems.addLayer(layer);

    if (label !== "") {
        layer.bindTooltip(label, {
            permanent: true, 
            direction: 'top',
            offset: [0, -15],
            className: 'map-label'
        }).openTooltip();
    }
});
