import React, { Component } from 'react';
import Map from './components/Map';
import Menu from './components/Menu';

const ZOMATO_API_KEY = 'b95ab0780f238e8875f0686727f6ef80';
const ZOMATO_API_URL = 'https://developers.zomato.com/api/v2.1/search?q=sushi&count=50&lat=49.2501&lon=-123.0824&radius=100000';

class App extends Component {
  constructor(props) {
    super(props);
    this.state = {
      items: [],
      inputFilter: '',
      selectItem: null
    }
  }

  /**
   * Fetch restaurant data from zomato.com
   */
  componentDidMount() {
    fetch(ZOMATO_API_URL, { 
      headers: new Headers({
        'user-key': ZOMATO_API_KEY,
        'Accept': 'application/json'
      })
    })
      .then(res => res.json())
      .then(
        (result) => {
          this.setState({
            items: result.restaurants,
          })
        },
        (error) => {
          alert("There's something wrong to fetch data from Zomato.\nCheck your internet connection or contact your admin.")
        }
      )
  }

  _updateFilterItem = (value) => {
    this.setState({
      inputFilter: value,
      selectItem: null
    });
  }

  _updateSelectItem = (value) => {
    this.setState({
      selectItem: value
    });
  }

  render() {
    return (
      <main id="app">
        <Menu {...this.state} 
          onFilterChange={this._updateFilterItem}
          onSelectChange={this._updateSelectItem}></Menu>
        <Map {...this.state}
          onSelectChange={this._updateSelectItem}></Map>
      </main>
    )
  }
}

export default App
