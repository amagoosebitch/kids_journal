import React from "react";
import { Header } from "../../components/header/Header";
import { useParams } from "react-router-dom";
import { ProgressList } from "../../components/progressList/ProgressList";

type ProgressPageProps = {};

function ProgressPage({}: ProgressPageProps): JSX.Element {
  const { organization, group, lesson } = useParams();
  return (
    <div>
      <Header />
      <ProgressList
        organization={organization}
        group={group}
        lesson={lesson}
      />
    </div>
  );
}

export default ProgressPage;
