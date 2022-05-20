import React from "react";
import autoBind from "auto-bind";
import urlJoin from "url-join";
import RSPANResultTable from "../components/export_table";
import { SelectStyle } from "../components/datatable";

import "./ExportScreen.css";

export default class ExportScreen extends React.Component {
  constructor(props) {
    super(props);
    autoBind(this);

    this.exportTableRef = React.createRef();
  }

  render() {
    return (
      <div className="export-screen">
        <RSPANResultTable
          tableId={"export-table"}
          selectStyle={SelectStyle.OS}
          ref={this.exportTableRef}
          initiateDataLoad={this.initiateDataLoad}
          onExportClicked={this.onExportClicked}
        />
      </div>
    );
  }

  async initiateDataLoad() {
    if (process.env.NODE_ENV !== "production") {
      return new Promise((resolve) => {
        setTimeout(() => {
          resolve([]);
        }, 1000);
      });
    } else {
      let resultUrl = "../api/result";

      if (process.env.PUBLIC_URL) {
        resultUrl = urlJoin(process.env.PUBLIC_URL, resultUrl);
      }

      const response = await fetch(resultUrl, {
        headers: {
          "X-HTTP-APIKEY": "9463d2d2-8560-40ea-8f4e-739ac9afed2c",
          "Content-Type": "application/json",
        },
      });
      const data = await response.json();
      return data;
    }
  }

  onExportClicked() {
    console.debug("export clicked");
    if (this.exportTableRef === null) return;
    else if (this.exportTableRef.current === null) return;
    else if (this.exportTableRef.current.getTable() === null) return;

    let selectedData = this.exportTableRef.current.getTable().getSelectedRows();
    let subjectIds = [];

    for (let i = 0; i < selectedData.length; i++) {
      let testRecord = selectedData[i];
      subjectIds.push(testRecord.subject_id);
    }

    let subjectIdString = subjectIds.join(",");

    console.debug("Exporting test data gathered from selected rows: ");
    console.debug(selectedData);
    console.debug(subjectIdString);

    let exportUrl = "download?subject_ids=" + subjectIds;

    if (process.env.PUBLIC_URL) {
      exportUrl = urlJoin(process.env.PUBLIC_URL, exportUrl);
    }

    window.location = exportUrl;
  }
}
