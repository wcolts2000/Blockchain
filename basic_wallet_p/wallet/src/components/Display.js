import React from 'react'

export default function Display({chain, title, length, filterChain}) {
  

    if(chain.length) {

      return (
        <div>
          <h3>Total Blocks: {length}</h3>
          <h3>{title}</h3>
          <code>{JSON.stringify(chain)}</code>
        </div>
      )
    } else {
      return (
      <div>
        <h3>Total: Loading...</h3>
        <p>Loading...</p>
        </div>
      )
    }
}