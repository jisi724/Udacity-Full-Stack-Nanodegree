import imgIcon from './assets/icon.png';
import imgIconBlue from './assets/icon.svg';

let Utils = {};

/**
 * return a costom marker.
 */
Utils.getMarkerIcon = () => {
  const icon = document.createElement('img');
  icon.className = 'map-marker';
  icon.setAttribute('src', imgIcon);
  icon.setAttribute('alt', 'red mark icon');
  icon.addEventListener('click', () => {
    [...document.querySelectorAll('.map-marker')].map(marker => {
      marker.src = imgIcon;
    });
    icon.setAttribute('src', imgIconBlue);
  });

  return icon;
};

Utils.getPopUp = (data, mapboxgl) => {
  const popupHTML = `
    <div class="map-popup">
      <div class="map-popup-header" style="background-image: url(${data.featured_image})">
        <div>
          <h4>${data.name}</h4>
          <h5>${data.user_rating.aggregate_rating} / 5</h5>
        </div>
      </div>
      <div class="map-popup-info">
        <div>
          <h5 class="label">Address: </h5>
          <h5 class="value">${data.location.address}</h5>
        </div>
        <div>
          <h5 class="label">Average Cost: </h5>
          <h5 class="value">${data.cost}</h5>
        </div>
        <div>
          <a href=${data.menu_url} target="_blank" rel="noopener noreferrer">Check Menu</a>
          <a href=${data.url} target="_blank" rel="noopener noreferrer">Check Intro</a>
        </div>
      </div>
    </div>
  `;

  const popup = new mapboxgl.Popup({ offset: 25 }).setHTML(popupHTML);

  return popup;
};

export default Utils;
