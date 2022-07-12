import React, { useState } from "react";
import keycloak from "./Keycloak";
import {Link} from "react-router-dom";

const Create = () => {
    const proxyUrl = 'https://cors-anywhere.herokuapp.com/';
  const [service_type_id, setService] = useState('1');
  const [amount, setAmount] = useState('0');
  const [payment_method, set_payment_method] = useState('1');
  const [voucherPin, setVoucherPin] = useState('0');
  const [walletAddress, setWalletAddress] = useState('0');
  const [service_period_sec, setServicePeriod] = useState("0");
  const [package_name, setPackage] =useState("1GB 1min")

  const handleSubmit = (e) => {
      const username = keycloak.tokenParsed.preferred_username
      console.log(username)
      const keycloak_id = username
    e.preventDefault();
      let payment = { };
      if (payment_method === "1") {
          if (package_name === "1GB 1min") {
              payment = { keycloak_id, service_type_id, amount, payment_method, voucherPin, "package":package_name, service_period_sec };
          }
          payment = { keycloak_id, service_type_id, amount, payment_method, voucherPin, "package":package_name, service_period_sec };
      }
      else if (payment_method === "8") {
          if (package_name === "1GB 1min") {
              payment = { service_type_id, amount, payment_method, walletAddress, service_period_sec, "package":package_name };
          }

      }
      console.log(JSON.stringify(payment))
      fetch('http://0.0.0.0:8000/purchase/', {
      method: 'POST',
      body: JSON.stringify(payment)
    })
          .then(response => {
      console.log(response);
    })
  }

  return (
    <div className="create">
      <h2>Purchase</h2>
      <form onSubmit={handleSubmit}>
        <label>Service</label>
        <select
          required
          value={service_type_id}
          onChange={(e) => setService(e.target.value)}
        >
                      <option value="1">Internet</option>
            </select>



        <label>Amount</label>
        <input
            required
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
    />
        <label>Payment Method</label>
        <select
            required
          value={payment_method}
          onChange={(e) => set_payment_method(e.target.value)}
        >
          <option value="1">1ForYou</option>
          <option value="8">CIC</option>
        </select>
          {(payment_method === "1") && (<> <label>Voucher</label>
          <input required
                value={voucherPin}
                onChange={(e) => setVoucherPin(e.target.value)}
            /></>)
        }
        {(payment_method === "8") && (<> <label>Wallet Address</label> <input required
                value={walletAddress}
                onChange={(e) => setWalletAddress(e.target.value)}
            />

        </>)

        }
        <button>Purchase</button>
      </form>
<Link to="/">
            <button>Home Page</button></Link>
    </div>

  );
}

export default Create;