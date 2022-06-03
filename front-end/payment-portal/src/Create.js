import React, { useState } from "react";
import keycloak from "./Keycloak";
import {Link} from "react-router-dom";

const Create = () => {
  const [Service, setService] = useState('Internet');
  const [Amount, setAmount] = useState('0');
  const [paymentMethod, setPaymentMethod] = useState('1');

  return (
    <div className="create">
      <h2>Purchase</h2>
      <form>
        <label>Service</label>
        <select
          required
          value={Service}
          onChange={(e) => setService(e.target.value)}
        >
                      <option value="1">Internet</option>
            </select>
        <label>Amount</label>
        <input
    required
    value={Amount}
    onChange={(e) => setAmount(e.target.value)}
    />
        <label>Payment Method</label>
        <select
            required
          value={paymentMethod}
          onChange={(e) => setPaymentMethod(e.target.value)}
        >
          <option value="1">1ForYou</option>
          <option value="8">CIC</option>
        </select>
          {(paymentMethod === "1") && (<> <label>Voucher</label>
          <input type="text" required/></>)

        }
        {(paymentMethod === "8") && (<> <label>Wallet Address</label>
          <input type="text" required/></>)

        }
        <button>Purchase</button>
      </form>
<Link to="/">
            <button>Home Page</button></Link>
    </div>

  );
}

export default Create;