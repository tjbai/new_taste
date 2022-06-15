import React from 'react'
import './Song.css'

const SONG_HEADER = 'https://open.spotify.com/track/'

const Song = ({id, genre, title, artist}) => {

    const link = SONG_HEADER+id;

    return (
        <div 
            className='songIndicator'
            style={{
                width: '80%',
                height: '100px',
                backgroundColor: 'black',
                margin: '10px',
                borderRadius: '20px',
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'center',
                alignItems: 'flex-start',
                padding: '20px',
            }} 
        >
            <a href={link} target='_blank' id='tag'>
                <div style={{
                    fontSize: '20px',
                }}>{title}</div>

                <div style={{
                    fontSize: '15px',
                }}>by {artist} ({genre})</div>
            </a>
        </div>
    )
}

export default Song