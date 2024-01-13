import React from "react";
import { Header } from "../../components/header/Header";
import { Groups } from "../../components/groups/Groups";
import { useParams } from "react-router-dom";

type GroupsPageProps = {};

function GroupsPage({}: GroupsPageProps): JSX.Element {
  const { organization } = useParams();
  console.log(organization);
  return (
    <div>
      <Header />
      <Groups organization={organization}/>
    </div>
  );
}

export default GroupsPage;
