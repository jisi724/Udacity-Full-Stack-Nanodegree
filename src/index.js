/* global ko */

import './index.css';
import mapboxgl from 'mapbox-gl/dist/mapbox-gl';
import Utils from './helper';

const MAPBOX_API_KEY = 'pk.eyJ1IjoiamlzaTcyNCIsImEiOiJjaW83bmRjODEwMnBodmdrcWlmc2M2NTF1In0.diflnHFyCHTX4yUOeuZOlg';
const ZOMATO_API_KEY = 'b95ab0780f238e8875f0686727f6ef80';
const ZOMATO_API_URL = 'https://developers.zomato.com/api/v2.1/search?q=sushi&count=50&lat=49.2501&lon=-123.0824&radius=100000';

let markers = [];

/**
 * Init Mapbox Map
 */
function initMapbox () {
  mapboxgl.accessToken = MAPBOX_API_KEY;
  let map = new mapboxgl.Map({
    container: 'mapContainer',
    style: 'mapbox://styles/mapbox/basic-v9',
    center: [-123.1107, 49.2727],
    zoom: 12
  });
  let nav = new mapboxgl.NavigationControl();
  map.addControl(nav, 'top-right');

  return map;
}

/**
 * Fetch restaurants information from Zomato.com
 *
 * @param {requestCallback} callback - the callback that handle returned data from KO
 */
function fetchData (callback) {
  fetch(ZOMATO_API_URL, {
    headers: new window.Headers({
      'user-key': ZOMATO_API_KEY,
      'Accept': 'application/json'
    })
  })
    .then(res => res.json())
    .then(
      result => callback(result.restaurants),
      () => alert("There's something wrong to fetch data from Zomato.\nCheck your internet connection or contact your admin.")
    );
}

function closeAllPopups () {
  markers.forEach(marker => {
    const popup = marker.getPopup();
    marker.getElement().src = '/src/assets/icon.png';
    if (popup.isOpen()) {
      marker.togglePopup();
    }
  });
}

/**
 * knockout ViewModel
 */
function AppViewModel () {
  this.showMenu = ko.observable(true);
  this.inputFilterText = ko.observable('');
  this.restaurants = ko.observableArray([]);

  this.toggleMenu = () => this.showMenu(!this.showMenu());

  this.handleMenuClick = (restaurant) => {
    console.log(restaurant.restaurant.name());
    restaurant.popup(!restaurant.popup());
  };

  this.filteredResult = ko.computed(() => {
    const filter = this.inputFilterText().toLowerCase();
    return ko.utils.arrayFilter(this.restaurants(), restaurant => {
      const restaurantName = restaurant.restaurant.name().toLowerCase();
      if (restaurantName.indexOf(filter) !== -1) {
        restaurant.visiable(true);
        return true;
      } else {
        restaurant.visiable(false);
        return false;
      }
    });
  });

  const map = initMapbox();

  /**
   * fetch data in viewModel, and add markers in the callback
   */
  fetchData(restaurants => {
    if (restaurants) {
      restaurants.forEach(item => {
        const location = item.restaurant.location;
        const popup = Utils.getPopUp(item.restaurant, mapboxgl);
        const marker = new mapboxgl.Marker(Utils.getMarkerIcon())
          .setLngLat([location.longitude, location.latitude])
          .setPopup(popup)
          .addTo(map);
        markers.push(marker);

        const markerDom = marker.getElement();

        // mapping fetched properties as observables
        let data = ko.mapping.fromJS(item);

        // add a visiable property then subscribe it to control marker's visibility.
        data.visiable = ko.observable(true);
        data.visiable.subscribe(visiable => visiable ? marker.addTo(map) : marker.remove());

        // add a popup property then subscripbe it so that clicks on list can open the popup.
        data.popup = ko.observable(false);
        data.popup.subscribe(() => {
          if (!popup.isOpen()) {
            closeAllPopups();
            markerDom.src = '/src/assets/icon.svg';
            marker.togglePopup();
          }
        });

        // push fetched and entended object to this.restaurants
        this.restaurants.push(ko.mapping.fromJS(data));
      });
    }
  });
}

ko.applyBindings(new AppViewModel());
