import React from 'react';
import ReactMapGL, { Marker, WebMercatorViewport, FlyToInterpolator } from 'react-map-gl';
import { easeCubic } from 'd3-ease';
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faMapMarkerAlt, faMapPin } from '@fortawesome/free-solid-svg-icons';

import './Map.css';

const Map = (
  {
    selectedEvent
  }
) => {

  const [
    viewport,
    setViewport
  ] = React.useState({
    width: '100%',
    height: '100vh',
    latitude: 0,
    longitude: 0,
    zoom: 10
  });

  const [
    userPosition,
    setUserPosition
  ] = React.useState();

  React.useEffect(
    () => {
      if (userPosition !== undefined) {
        setViewport({
          ...viewport,
          ...userPosition
        })
      }
    },
    [userPosition]
  )

  React.useEffect(
    () => {
      if (selectedEvent !== undefined && 
        selectedEvent.location.latitude !== '' && 
        selectedEvent.location.longitude !== '') {
        const {
          longitude,
          latitude,
          zoom
        } = new WebMercatorViewport(viewport).fitBounds(
          [[userPosition.longitude, userPosition.latitude], [selectedEvent.location.longitude, selectedEvent.location.latitude]],
          {
            padding: 20,
            offset: [0, -100]
          }
        )

        setViewport({
          ...viewport,
          longitude,
          latitude,
          zoom,
          transitionDuration: 2000,
          transitionInterpolator: new FlyToInterpolator(),
          transitionEasing: easeCubic
        })
      }
    },
    [selectedEvent]
  )

  React.useEffect(() => {
    navigator.geolocation.getCurrentPosition(pos => {
      setUserPosition({
        latitude: pos.coords.latitude,
        longitude: pos.coords.longitude
      })
    });
  }, [])

  return (
    <div
      className='map'
    >
      <ReactMapGL
        mapStyle='mapbox://styles/mapbox/streets-v10'
        {...viewport}
        onViewportChange={viewport => setViewport(viewport)}
      >
        {userPosition && (
          <Marker
            latitude={userPosition.latitude}
            longitude={userPosition.longitude}
          >
            <FontAwesomeIcon icon={faMapMarkerAlt} className='map-marker' />
          </Marker>
        )
        }
        {selectedEvent && 
        selectedEvent.location.latitude !== '' &&
        selectedEvent.location.longitude !== '' && (
          <Marker
            latitude={selectedEvent.location.latitude}
            longitude={selectedEvent.location.longitude}
          >
            <FontAwesomeIcon icon={faMapPin} className='map-marker' />
          </Marker>
        )}
      </ReactMapGL>
    </div>
  );
};

export default Map;
