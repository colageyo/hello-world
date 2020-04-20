import React from 'react';
import { Link } from 'react-router-dom';
import './HelloWorldToolBar.css';
import './App.css';
import Logo from './assets/logo_day.png';

function HelloWorldToolBar() {
    return (
      <div className="nav-bar small-content">
        <Link
          to='/'
        >
          <img className="logo" src={Logo}/>
        </Link>
        <div className="text-container">
          <div className="text tool-bar-text button">
            <Link
              to='/recommend'
            >
              Activities and Events
            </Link>
          </div>
          <div className="text tool-bar-text button">Contact Us</div>
        </div>
      </div>
    );
}

export default HelloWorldToolBar;
