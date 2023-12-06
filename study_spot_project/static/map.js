/**
 * @license
 * Copyright 2019 Google LLC. All Rights Reserved.
 * SPDX-License-Identifier: Apache-2.0
 */
// This example displays markers for multiple places on the map.

function initMap() {

  const map = new google.maps.Map(document.getElementById("map"), {
    zoom: 15,
    center: { lat: 38.03288, lng: -78.50756 },
  });

  var lastOpenedWindow = null;

  places.forEach((place) => {
    const url = `/${place.name_slug}/details`;
  
    
    const contentString = `
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.3/dist/css/bootstrap.min.css" rel="stylesheet">
    <link href="https://getbootstrap.com/docs/5.2/assets/css/docs.css" rel="stylesheet">
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.16.0/umd/popper.min.js"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js"></script>
    <div id="content" style="background-color: #bbe2c6; color: #000; padding: 20px;">
      <div id="siteNotice"></div>
      <h1 id="firstHeading" class="firstHeading text-center" style="background-color: #bbe2c6; font-size: 20px;">
        ${place.name}
      </h1>
      <div id="bodyContent">
        <a href="${url}" class="btn btn-success" style="text-decoration: none; color: #0; font-size: 15px;">View Study Spot Details</a>
      </div>
    </div>`;


    const infowindow = new google.maps.InfoWindow({
      content: contentString,
      ariaLabel: place.name,
    });

    const marker = new google.maps.Marker({
      position: { lat: parseFloat(place.lat), lng: parseFloat(place.long)},
      map,
      title: place.name,
    });

    marker.addListener("click", () => {
      if (lastOpenedWindow == infowindow) {
        infowindow.close();
        lastOpenedWindow = null;
        return;
      }
      if (lastOpenedWindow) {
        lastOpenedWindow.close();
      }
      infowindow.open({
        anchor: marker,
        map,
      });
      
      lastOpenedWindow = infowindow;
    });


  });
}

window.initMap = initMap;