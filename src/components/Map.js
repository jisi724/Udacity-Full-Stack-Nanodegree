import React, {Component} from 'react';
import MapGL, {Marker, Popup, NavigationControl} from 'react-map-gl';
import 'mapbox-gl/dist/mapbox-gl.css';
import MapPopup from './MapPopup';
import pin from '../assets/icon.png';

const MAPBOX_API_KEY = "pk.eyJ1IjoiamlzaTcyNCIsImEiOiJjaW83bmRjODEwMnBodmdrcWlmc2M2NTF1In0.diflnHFyCHTX4yUOeuZOlg";

class Map extends Component {
  constructor(props) {
    super(props);
    this.state = {
      viewport: {
        width: '100%',
        height: '100vh',
        latitude: 49.2727,
        longitude: -123.1107,
        zoom: 12
      }
    }
  }

  _updateViewport = (viewport) => {
    this.setState({viewport});
  }

  _selectChangeHandler = (e) => {
    this.props.onSelectChange(e);
  }

  _renderMarkers = () => {
    const markers = this.props.items.filter((i) => {
      return i.restaurant.name.toLowerCase().indexOf(this.props.inputFilter.toLowerCase()) !== -1;
    }).map((item, index) => {
      const location = item.restaurant.location
      return (
        <Marker 
          latitude={parseFloat(location.latitude)} 
          longitude={parseFloat(location.longitude)}
          key={index}>
          <img src={pin} className='map-marker' alt='blue marker'
               onClick={() => this._selectChangeHandler(item.restaurant.R.res_id)}/>
        </Marker>
      )
    })
    return markers;
  }

  _renderPopupWindow = () => {
    if (this.props.selectItem) {
      let currentPopup = null
      this.props.items.forEach((item) => {
        if (item.restaurant.R.res_id === this.props.selectItem) {
          const restaurant = item.restaurant
          currentPopup = {
            latitude: parseFloat(restaurant.location.latitude),
            longitude: parseFloat(restaurant.location.longitude),
            name: restaurant.name,
            cost: parseFloat(restaurant.average_cost_for_two)/2,
            image: restaurant.featured_image,
            address: restaurant.location.address,
            menuUrl: restaurant.menu_url,
            introUrl: restaurant.url,
            rate: restaurant.user_rating.aggregate_rating
          }
        }
      })
      return (
        <Popup
        longitude={currentPopup.longitude}
        latitude={currentPopup.latitude}
        closeOnClick={false}
        onClose={() => this._selectChangeHandler(null)}>
          <MapPopup restaurant={currentPopup}></MapPopup>
        </Popup>
      )
    }
  }

  render() {
    return (
      <section className='map'>
        <MapGL
          {...this.state.viewport}
          mapboxApiAccessToken={MAPBOX_API_KEY}
          mapStyle="mapbox://styles/mapbox/basic-v9"
          onViewportChange={this._updateViewport}>

          <div className="map-nav">
            <NavigationControl onViewportChange={this._updateViewport} />
          </div>

          {this._renderMarkers()}

          {this._renderPopupWindow()}

        </MapGL>
      </section>
    )
  }
}

export default Map