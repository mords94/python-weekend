import './App.css';
import { Form } from 'semantic-ui-react';
import { useReducer, useCallback, useState } from 'react';
import DatePicker from 'react-datepicker';

import 'react-datepicker/dist/react-datepicker.css';

function reducer(state, action) {
  console.log({ state, action });
  switch (action.type) {
    case 'setSource':
      return { ...state, source: action.payload };
    case 'setDestination':
      return { ...state, destination: action.payload };
    case 'setDeparture':
      return { ...state, departure: action.payload };
    default:
      throw new Error();
  }
}

function App() {
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState([]);
  const [submitted, setSubmitted] = useState(false);

  const [formValues, dispatch] = useReducer(reducer, {
    source: 'Brno',
    destination: 'Prague',
    departure: new Date(),
  });

  const { source, destination, departure } = formValues;

  const handleSubmit = useCallback(() => {
    setSubmitted(true);
    const fetchResults = async () => {
      try {
        setLoading(true);
        const result = await fetch(
          `/search?source=${source}&destination=${destination}&departure_date=${
            departure.toISOString().split('T')[0]
          }`
        );

        setResults(await result.json());
      } catch {
      } finally {
        setLoading(false);
      }
    };

    fetchResults();
  }, [departure, destination, source]);

  return (
    <div className="App">
      <div className="wrapper">
        <h1 class="ui header">Python weekend</h1>
        <Form onSubmit={handleSubmit}>
          <Form.Group>
            <Form.Input
              placeholder="Source"
              name="source"
              value={source}
              disabled={loading}
              onChange={(e) => {
                dispatch({ type: 'setSource', payload: e.target.value });
              }}
            />
            <Form.Input
              placeholder="Destination"
              name="destination"
              value={destination}
              disabled={loading}
              onChange={(e) => {
                dispatch({ type: 'setDestination', payload: e.target.value });
              }}
            />
            <DatePicker
              selected={departure}
              dateFormat="yyyy-MM-dd"
              disabled={loading}
              onChange={(date) => {
                dispatch({ type: 'setDeparture', payload: date });
              }}
            />
            <Form.Button
              content="Search"
              disabled={loading}
              loading={loading}
            />
          </Form.Group>
        </Form>
        {!loading && submitted && results.length === 0 && (
          <div className="item">
            <h1 class="ui header">No result for this criteria</h1>
          </div>
        )}
        {!loading &&
          results.map((result) => (
            <div className="item">
              <div>
                <h1 class="ui header">
                  {result.source} - {result.destination}
                </h1>
                <div>
                  Departure:{' '}
                  {new Date(result.departure_datetime).toLocaleTimeString()}{' '}
                  {new Date(result.departure_datetime).toLocaleDateString()}
                </div>

                <div>
                  Arrival:{' '}
                  {new Date(result.arrival_datetime).toLocaleTimeString()}{' '}
                  {new Date(result.arrival_datetime).toLocaleDateString()}
                </div>
              </div>

              <h3 class="ui header">
                {result.fare.amount} {result.fare.currency}
              </h3>
            </div>
          ))}
      </div>
    </div>
  );
}

export default App;
