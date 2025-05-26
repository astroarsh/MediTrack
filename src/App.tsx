import React from 'react';
import { BrowserRouter as Router, Route, Switch } from 'react-router-dom';
import HomeScreen from './HomeScreen';
import AdminLogin from './components/AdminLogin';
import DoctorLogin from './components/DoctorLogin';
import PatientLogin from './components/PatientLogin';
import SignUp from './components/SignUp';

const App: React.FC = () => {
    return (
        <Router>
            <Switch>
                <Route path="/" exact component={HomeScreen} />
                <Route path="/admin-login" component={AdminLogin} />
                <Route path="/doctor-login" component={DoctorLogin} />
                <Route path="/patient-login" component={PatientLogin} />
                <Route path="/sign-up" component={SignUp} />
            </Switch>
        </Router>
    );
};

export default App;