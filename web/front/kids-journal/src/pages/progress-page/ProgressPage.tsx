import React from "react";
import { Header } from "../../components/header/Header";
import { useParams } from "react-router-dom";
import {ProgressList} from "../../components/progressList/ProgressList";

type ProgressPageProps = {};

function ProgressPage({}: ProgressPageProps): JSX.Element {
    const { organization } = useParams();
    return (
        <div>
            <Header />
            <ProgressList organization={organization}/>
        </div>
    );
}

export default ProgressPage;
