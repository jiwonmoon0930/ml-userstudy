
import React, { Component } from "react";
import { HashRouter, Router, Switch, Route} from 'react-router-dom';

// import TaskContainer from './pages/task-selection/task-selection';
import StartContainer from './pages/start/start';
import InstructionsContainer from './pages/instr/instructions';
import Main1Container from "./pages/main/main-task1";
import Main2Container from "./pages/main/main-task2";
import Main3Container from "./pages/main/main-task3";
import SurveyContainer from "./pages/survey/survey"
import EndContainer from "./pages/end/end";


export default class Routes extends Component {
    render() {
        return (
            <HashRouter>
                <Switch>
                    <Route path="/" exact component={StartContainer} />
                    <Route path="/Instructions" component={InstructionsContainer} />
                    <Route path="/Main1" component={Main1Container} />
                    <Route path="/Main2" component={Main2Container} />
                    <Route path="/Main3" component={Main3Container} />
                    <Route path="/Survey" component={SurveyContainer} />
                    <Route path="/End" component={EndContainer} />

                </Switch>
            </HashRouter>

        )
    }
}