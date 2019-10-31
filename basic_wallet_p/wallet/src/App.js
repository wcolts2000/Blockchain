import React, { Component } from 'react';
import Display from './components/Display';
import Form from './components/Form';
import axios from "axios";

class App extends Component {
  state={
    chain: [],
    title: "Whole Chain",
    filteredChain: [],
    id: null
  }

  componentDidMount() {
    this.getChain()
  }

  getChain = () => {
    axios.get('http://localhost:5000/chain')
    .then(({data}) => this.setState({chain: data}))
    .catch(err => console.error(err))
  }

  filterChain = (id) => {
    console.log("CHAIN: ", this.state.chain, "\n id: ", id)
    const filteredChain = this.state.chain.chain.filter(block => {
      console.log("block: ", block)
      if (!block.transactions.length) {
        return false
      }
      else {
        return block.transactions[0].recipient === id
      } 
    })
    this.setState(
      {
        id,
        title: `${id}'s Transactions`,
        filteredChain
      }
      )
  } 

  render() {
    return (
      <div className="App">
        <Form 
          filterChain={this.filterChain}
        />
        <Display 
          chain={this.state.filteredChain.length ? this.state.filteredChain : this.state.chain}
          title={this.state.title}
          length={this.state.chain.length}
        />
      </div>
    );
  }
}

export default App;
