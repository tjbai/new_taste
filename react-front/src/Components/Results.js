import React from 'react';

export const Results = (state) => {
    console.log(state.state.songs)

    return (
        <div>
            <p>NUM FACES = {state.state.faceCount}</p>
            <p>EMOS = {JSON.stringify(state.state.emotions)}</p>
            <img src={state.state.faceImg} />
            <ul>
                <li>TEST1</li>
                {state.state.songs.map((s) => 
                    <li key={s[0]}> {s[2]} by {s[3]} </li>)
                }
                <li>TEST2</li>
            </ul>
        </div>
    )
}