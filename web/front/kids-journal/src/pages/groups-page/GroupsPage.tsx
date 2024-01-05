import React from "react";
import { Header } from "../../components/header/Header";
import { Groups } from "../../components/groups/Groups";

type GroupsPageProps = {};

function GroupsPage({}: GroupsPageProps): JSX.Element {
  return (
    <div>
      <Header />
      <Groups />
    </div>
  );
}

export default GroupsPage;
