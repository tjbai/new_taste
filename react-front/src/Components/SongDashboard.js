import React from 'react';
import Song from './Song'
import './SongDashboard.css'

const SongDashboard = ({songs}) => {
    return (    
        <div 
            id='songDashboard'
            style={{
                display: 'flex',
                flexDirection: 'column',
                justifyContent: 'space-evenly',
                alignItems: 'center',
                backgroundColor: '#1DB954',
                borderRadius: '20px',
                height: '400px',
                width: '300px'
            }}
        >
            {songs.map(s => 
                <Song
                    id={s[0]}
                    genre={s[1]}
                    title={s[2]}
                    artist={s[3]}
                />
            )}
        </div>
    )
}

export default SongDashboard