import React, { Component } from 'react';

class MapPopup extends Component {
  render() {
    const data = this.props.restaurant;

    const backgroundStyle = {
      backgroundImage: 'url(' + data.image + ')'
    }


    return (
      <div className="map-popup">
        <div className="map-popup-header" style={backgroundStyle}>
          <div>
            <h4>{data.name}</h4>
            <h5>{data.rate} / 5</h5>
          </div>
        </div>
        <div className="map-popup-info">
          <div>
            <h5 className="label">Address: </h5>
            <h5 className="value">{data.address}</h5>
          </div>
          <div>
            <h5 className="label">Average Cost: </h5>
            <h5 className="value">${data.cost}</h5>
          </div>
          <div>
            <a href={data.menuUrl} target="_blank" rel="noopener noreferrer">Check Menu</a>
            <a href={data.introUrl} target="_blank" rel="noopener noreferrer">Check Intro</a>
          </div>
        </div>
      </div>
    )
  }
}

export default MapPopup;