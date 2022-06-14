import React from 'react';

export const Results = (state) => {
    return (
        <div>
            <p>NUM FACES = {state.state.faceCount}</p>
            <p>EMOS = {JSON.stringify(state.state.emotions)}</p>
            <img src={state.state.faceImg} />
            <ul>
                {state.state.songs.map((s) => 
                    <li key={s[0]}> 
                        {s[2]} by {s[3]} 
                    </li>
                )}
            </ul>
        </div>
    )
}

export default Results;