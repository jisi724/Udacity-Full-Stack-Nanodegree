import React, { Component } from 'react';
import toggle from '../assets/toggle.png';
import lookup from '../assets/loopup.png';

class Menu extends Component {
  constructor(props) {
    super(props);
    this.state = {
      showMenu: true,
    };
  }

  _renderItemList = () => {
    const finalList = this.props.items.filter((i) => {
      return i.restaurant.name.toLowerCase().indexOf(this.props.inputFilter.toLowerCase()) !== -1;
    })
    if (finalList.length > 0) {
      return finalList.map((item, index) => {
        const resturant = item.restaurant;
        const ifSelect = this.props.selectItem === resturant.R.res_id;
        return (
          <div className={"menu-list-item " + (ifSelect ? "selected" : "")} key={index} 
               onClick={() => this._selectChangeHandler(resturant.R.res_id)}>
            <h5>{resturant.name}</h5>
          </div>
        )
      })
    } else {
      return (
        <h5>No result.</h5>
      )
    }

  }

  _filterChangeHandler = (e) => {
    this.props.onFilterChange(e.target.value);
  }

  _selectChangeHandler = (e) => {
    this.props.onSelectChange(e);
  }

  render() {
    return (
      <section className="menu" style={{ transform: this.state.showMenu ? 'translateX(0)' : 'translateX(-265px)' }}>
        <div className="menu-heading">
          <h2>Neighborhood App</h2>
          <h4>Find the best SUSHI in Vancouver!</h4>
        </div>

        <div className="menu-filter">
          <input type="text" placeholder="Input Filter" 
                 value={this.state.inputFilter} onChange={this._filterChangeHandler}></input>
          <img src={lookup} alt="a search icon"></img>
        </div>

        <div className="menu-list">
          {this._renderItemList()}
        </div>

        <div className='menu-toggle' onClick={() => this.setState({showMenu: !this.state.showMenu})}>
          <img src={toggle} alt="Three lines menu icon"></img>
        </div>
      </section>
    );
  }
}

export default Menu;