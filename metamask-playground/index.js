/*
    adapted from http://eddmann.com/posts/promisifying-error-first-asynchronous-callbacks-in-javascript/
*/
const promisify = (func, ...args) =>
  new Promise((resolve, reject) =>
    func(...args, (err, value) =>
      (err ? reject(err) : resolve(value))
    )
  )

const p = (s) => {
  const p = document.createElement('p');
  p.innerText = s || '';
  return p;
}
const body = document.body;

const printInfo = () => {
  promisify(web3.version.getNetwork)
    .then(id => {
      let s = 'Using chain: ';

      // Network list at 
      // https://ethereum.stackexchange.com/questions/17051/how-to-select-a-network-id-or-is-there-a-list-of-network-ids
      switch (parseInt(id, 10)) {
        case 0:
          s += 'Pre-Release (Olympic - 0) [DEPRECATED]';
          break;
        case 1:
          s += 'Main net (1)';
          break;
        case 2:
          s += 'Morden Testnet (2) [DEPRECATED]';
          break;
        case 3:
          s += 'Ropsten Testnet (3) [POW]';
          break;
        case 4:
          s += 'Rinkeby Testnet (4) [POA]';
          break;
        case 42:
          s += 'Kovan Testnet (42) [POA]';
          break;
        case 77:
          s += 'Sokol Testnet (77) [POA]';
          break;
        case 99:
          s += 'Core (99) [POA]';
          break;
        case 7762959:
          s += 'Musicoin (7762959)';
          break;

        default:
          s += `Private chain (${id})`;
          break;
      }
      body.appendChild(p(s));
    })
    .then(() => promisify(web3.version.getNode))
    .then(s => body.appendChild(p(s)))
    .then(() => web3.eth.defaultAccount)
    .then(s => body.appendChild(p(`Default account: ${s}`)))
    .then(() => promisify(web3.eth.getAccounts))
    .then(l => l.length > 0 ? body.appendChild(p('Accounts: ' + l.join(', '))) : body.appendChild(p('No accounts')))
    .then(() => promisify(web3.eth.getAccounts))
    .then(l => Promise.all(l.map(a => Promise.all([Promise.resolve(a), promisify(web3.eth.getBalance, a)]))))
    .then(l => l.length > 0 ? (body.appendChild(p('Account balances:')) && l.forEach(x => body.appendChild(p(`> ${x[0]}: ${x[1]}`)))) : null)
    .catch(err => body.appendChild(p(err)))
}



window.onload = () => {
  // Checking if Web3 has been injected by the browser (Mist/MetaMask)
  if (typeof web3 !== 'undefined') {
    // Use Mist/MetaMask's provider
    body.appendChild(p(web3.currentProvider.isMetaMask ? 'Using metamask' : 'Using dapp enabled browser'));
    web3 = new Web3(web3.currentProvider);
  } else {
    body.appendChild(p('Not on Mist nor Metamask connected'));
    web3 = new Web3(new Web3.providers.HttpProvider('https://ropsten.infura.io/***REMOVED***'));
  }
  printInfo();
};