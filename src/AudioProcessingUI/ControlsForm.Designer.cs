namespace AudioProcessingUI
{
    partial class ControlsForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.label1 = new System.Windows.Forms.Label();
            this.chooseDirButton = new System.Windows.Forms.Button();
            this.go = new System.Windows.Forms.Button();
            this.label2 = new System.Windows.Forms.Label();
            this.sourcePathTextbox = new System.Windows.Forms.TextBox();
            this.destPathTextbox = new System.Windows.Forms.TextBox();
            this.chooseDestinationButton = new System.Windows.Forms.Button();
            this.containsTextbox = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.SuspendLayout();
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(12, 12);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(169, 13);
            this.label1.TabIndex = 0;
            this.label1.Text = "Папка со звуками для анализа:";
            // 
            // chooseDirButton
            // 
            this.chooseDirButton.Location = new System.Drawing.Point(485, 9);
            this.chooseDirButton.Name = "chooseDirButton";
            this.chooseDirButton.Size = new System.Drawing.Size(75, 20);
            this.chooseDirButton.TabIndex = 1;
            this.chooseDirButton.Text = "Выбрать";
            this.chooseDirButton.UseVisualStyleBackColor = true;
            this.chooseDirButton.Click += new System.EventHandler(this.chooseDirButton_Click);
            // 
            // go
            // 
            this.go.Location = new System.Drawing.Point(460, 142);
            this.go.Name = "go";
            this.go.Size = new System.Drawing.Size(100, 52);
            this.go.TabIndex = 2;
            this.go.Text = "Поехали";
            this.go.UseVisualStyleBackColor = true;
            this.go.Click += new System.EventHandler(this.button2_Click);
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(12, 40);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(134, 13);
            this.label2.TabIndex = 4;
            this.label2.Text = "Сохранить результаты в:";
            // 
            // sourcePathTextbox
            // 
            this.sourcePathTextbox.Location = new System.Drawing.Point(187, 9);
            this.sourcePathTextbox.Name = "sourcePathTextbox";
            this.sourcePathTextbox.Size = new System.Drawing.Size(292, 20);
            this.sourcePathTextbox.TabIndex = 5;
            // 
            // destPathTextbox
            // 
            this.destPathTextbox.Location = new System.Drawing.Point(187, 37);
            this.destPathTextbox.Name = "destPathTextbox";
            this.destPathTextbox.Size = new System.Drawing.Size(292, 20);
            this.destPathTextbox.TabIndex = 6;
            // 
            // chooseDestinationButton
            // 
            this.chooseDestinationButton.Location = new System.Drawing.Point(485, 37);
            this.chooseDestinationButton.Name = "chooseDestinationButton";
            this.chooseDestinationButton.Size = new System.Drawing.Size(75, 20);
            this.chooseDestinationButton.TabIndex = 7;
            this.chooseDestinationButton.Text = "Выбрать";
            this.chooseDestinationButton.UseVisualStyleBackColor = true;
            this.chooseDestinationButton.Click += new System.EventHandler(this.chooseDestinationButton_Click);
            // 
            // containsTextbox
            // 
            this.containsTextbox.Location = new System.Drawing.Point(187, 83);
            this.containsTextbox.Name = "containsTextbox";
            this.containsTextbox.Size = new System.Drawing.Size(189, 20);
            this.containsTextbox.TabIndex = 8;
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(9, 86);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(159, 13);
            this.label3.TabIndex = 9;
            this.label3.Text = "Если в названии содержится:";
            // 
            // ControlsForm
            // 
            this.AutoScaleDimensions = new System.Drawing.SizeF(6F, 13F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.ClientSize = new System.Drawing.Size(567, 206);
            this.Controls.Add(this.label3);
            this.Controls.Add(this.containsTextbox);
            this.Controls.Add(this.chooseDestinationButton);
            this.Controls.Add(this.destPathTextbox);
            this.Controls.Add(this.sourcePathTextbox);
            this.Controls.Add(this.label2);
            this.Controls.Add(this.go);
            this.Controls.Add(this.chooseDirButton);
            this.Controls.Add(this.label1);
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.FixedDialog;
            this.Name = "ControlsForm";
            this.Text = "ControlsForm";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button chooseDirButton;
        private System.Windows.Forms.Button go;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.TextBox sourcePathTextbox;
        private System.Windows.Forms.TextBox destPathTextbox;
        private System.Windows.Forms.Button chooseDestinationButton;
        private System.Windows.Forms.TextBox containsTextbox;
        private System.Windows.Forms.Label label3;
    }
}