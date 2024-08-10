# Cartesi Olympics Medals Predictor DApp

This example shows a simple way of leveraging some of the most widely used Machine Learning libraries available in Python.

The DApp generates a [linear regression](https://en.wikipedia.org/wiki/Linear_regression) model using [scikit-learn](https://scikit-learn.org/), and [pandas](https://pandas.pydata.org/), and then uses [m2cgen (Model to Code Generator)](https://github.com/BayesWitnesses/m2cgen) to transpile that model into native Python code with no dependencies.
This approach is inspired by [Davis David's Machine Learning tutorial](https://www.freecodecamp.org/news/transform-machine-learning-models-into-native-code-with-zero-dependencies/), and is useful for a Cartesi DApp because it removes the need of porting all those Machine Learning libraries to the Cartesi Machine's RISC-V architecture, making the development process easier and the final back-end code simpler to execute.

This DApp is built on Cartesi to predict the number of medals a team might win in the Olympics based on the team's previous performance, number of athletes, and other features. Users interact with the DApp by sending input data through the Cartesi CLI. The DApp processes the inputs using a machine learning model and provides predictions via a `predict` endpoint. Additionally, users can query the `inspect` endpoint to retrieve all past predictions.

## Features

- **Prediction**: The model predicts the number of medals a team will win based on:
  - `team`: The team's name (e.g., "USA")
  - `athletes`: Number of athletes in the team
  - `prev_medals`: Number of medals won by the team in previous Olympics

- **Inspect Data**: The `inspect` endpoint returns all received predictions in a JSON format:
  ```json
  {
      "count": number,
      "predictions": [
          {
              "sender": "0x7...",
              "input": { 
                  "team": "USA", 
                  "athletes": 345, 
                  "prev_medals": 38 
              },
              "prediction": number
          }
      ]
  }
  ```

## Getting Started

Below you'll find instructions on how to set up this dApp locally.

### Prerequisites

Here are some packages you need to have installed on your PC:

* [Node.js](https://nodejs.org/en), [npm](https://docs.npmjs.com/cli/v10/configuring-npm/install), [yarn](https://classic.yarnpkg.com/lang/en/docs/install/#debian-stable)

* [Docker](https://docs.docker.com/get-docker/)

* [Cartesi CLI](https://docs.cartesi.io/cartesi-rollups/1.3/development/migration/#install-cartesi-cli)
  ```sh
  npm install -g @cartesi/cli
  ```

### Installation

1. Clone this repo
   ```sh
   git clone https://github.com/Ebukachuqz/cartesi-ml-olympics-predictor.git
   ```
  
2. Build and run the dApp via `cartesi-cli`
   ```sh
   cartesi build
   ```
   and
   ```sh
   cartesi run
   ```

### Interact with the DApp

- **Send Prediction Requests**:
  Use the Cartesi CLI to send input data in JSON format to predict the number of medals.
  ```json
  {
      "team": "USA",
      "athletes": 345,
      "prev_medals": 38
  }
  ```

  interact
    - *via `cartesi cli`*, access your terminal in another window and input these instructions below:
  
    ```sh
    cartesi send generic \
    --dapp=0xab7528bb862fb57e8a2bcd567a2e929a0be56a5e \
    --chain-id=31337 \
    --rpc-url=http://127.0.0.1:8545 \
    --mnemonic-passphrase="test test test test test test test test test test test junk" \
    --mnemonic-index=0 \
    --input='{ "team": "USA", "athletes":345, "prev_medals": 38}'
    ```

- **Inspect Past Predictions**:
  Retrieve all past predictions by querying the `/inspect` endpoint. The response will be in a hex `payload` that can be decoded to JSON as shown above.

  payload hex sample
  ```sh
  7b0d0a202020202020202022636f756e74223a20322c200d0a20202020202020202270726564696374696f6e73223a205b0d0a202020202020202020207b0d0a2020202020202020202020202273656e646572223a202230786633392e2e222c200d0a20202020202020202020202022696e707574223a207b0d0a2020202020202020202020202020227465616d223a2022555341222c200d0a2020202020202020202020202020226174686c65746573223a203334352c200d0a202020202020202020202020202022707265765f6d6564616c73223a2033380d0a2020202020202020202020207d2c200d0a2020202020202020202020202270726564696374696f6e223a2035320d0a202020202020202020207d2c200d0a202020202020202020207b0d0a2020202020202020202020202273656e646572223a2022307831352e2e2e222c0d0a20202020202020202020202022696e707574223a207b0d0a2020202020202020202020202020227465616d223a202242454c222c200d0a2020202020202020202020202020226174686c65746573223a203330352c200d0a202020202020202020202020202022707265765f6d6564616c73223a203134320d0a2020202020202020202020207d2c200d0a2020202020202020202020202270726564696374696f6e223a203132350d0a202020202020202020207d0d0a20202020202020205d0d0a2020202020207d
  ```

  ```json
      {
        "count": 2, 
        "predictions": [
          {
            "sender": "0xf39..", 
            "input": {
              "team": "USA", 
              "athletes": 345, 
              "prev_medals": 38
            }, 
            "prediction": 52
          }, 
          {
            "sender": "0x15...",
            "input": {
              "team": "BEL", 
              "athletes": 305, 
              "prev_medals": 142
            }, 
            "prediction": 125
          }
        ]
      }
  ```


## Model Details

- The prediction model uses **Linear Regression** to estimate the number of medals a team will win based on historical data, team size, and past performance.
- To ensure compatibility with the Cartesi machine, the model is converted into raw Python code using the `m2cgen` library, allowing it to run efficiently within the Cartesi framework.


## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Built using [Cartesi Rollups](https://docs.cartesi.io/cartesi-rollups/1.3/tutorials/machine-learning/).
