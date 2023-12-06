// https://snazzymaps.com/style/40976/no-businesses-or-points-of-interest
/**
 * @license
 * Copyright 2019 Google LLC. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
// This example displays markers for multiple places on the map.

var initialLat = parseFloat(document.getElementById('id_lat').value);
var initialLng = parseFloat(document.getElementById('id_long').value);
var map;
var marker;

google.maps.event.addDomListener(window, 'load', init);

function init() {
    var mapOptions;
    if (!isNaN(initialLat) && !isNaN(initialLng)) {
        mapOptions = {
            zoom: 15,
            center: new google.maps.LatLng(initialLat, initialLng),
            styles: [{"featureType":"administrative.neighborhood","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"poi","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"poi.park","elementType":"all","stylers":[{"visibility":"on"}]},{"featureType":"poi.park","elementType":"labels.text","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"all","stylers":[{"visibility":"on"}]},{"featureType":"transit","elementType":"labels.text","stylers":[{"visibility":"off"}]},{"featureType":"water","elementType":"all","stylers":[{"visibility":"on"}]}]
        };
    } else {
        mapOptions = {
            zoom: 15,
            center: new google.maps.LatLng(38.03288, -78.50756),
            styles: [{"featureType":"administrative.neighborhood","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"poi","elementType":"all","stylers":[{"visibility":"off"}]},{"featureType":"poi.park","elementType":"all","stylers":[{"visibility":"on"}]},{"featureType":"poi.park","elementType":"labels.text","stylers":[{"visibility":"off"}]},{"featureType":"transit","elementType":"all","stylers":[{"visibility":"on"}]},{"featureType":"transit","elementType":"labels.text","stylers":[{"visibility":"off"}]},{"featureType":"water","elementType":"all","stylers":[{"visibility":"on"}]}]
        };
    }

    var mapElement = document.getElementById('map');

    var map = new google.maps.Map(mapElement, mapOptions);

    if (!isNaN(initialLat) && !isNaN(initialLng)) {
        marker = new google.maps.Marker({
            position: { lat: initialLat, lng: initialLng },
            map: map,
            draggable: true
        });
    }

    map.addListener('click', function (event) {
        if (!marker) {
            marker = new google.maps.Marker({
                position: event.latLng,
                map: map,
                draggable: true
            });
        } else {
            marker.setPosition(event.latLng);
        }

        document.getElementById('id_lat').value = event.latLng.lat();
        document.getElementById('id_long').value = event.latLng.lng();
    });
}
google.maps.event.addDomListener(window, 'load', initializeMap);
