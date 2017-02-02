from django.db import models


# Create your models here.

class Species(models.Model):
    name = models.CharField(max_length=300)
    type = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Sample(models.Model):
    name = models.CharField(max_length=300)

    def __str__(self):
        return self.name


class ss_data(models.Model):
    sample = models.ForeignKey(Sample)
    species = models.ForeignKey(Species)
    count = models.IntegerField()

    def __str__(self):
        return self.species.name + " " + self.sample.name + " " + str(self.count)

class PCR_target(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class PCR_detail(models.Model):
    sample = models.ForeignKey(Sample)
    ward_1 = models.CharField(max_length=10, blank=True, null=True, default=None)
    ward_2 = models.CharField(max_length=10, blank=True, null=True, default=None)
    age = models.CharField(max_length=10, blank=True, null=True, default=None)
    PCR = models.CharField(max_length=10, blank=True, null=True, default=None)
    PCR_result = models.CharField(max_length=10, blank=True, null=True, default=None)
    RPPCR_date = models.IntegerField()


    def __str__(self):
        return self.sample.name

class PCR_data(models.Model):
    sample = models.ForeignKey(Sample)
    target = models.ForeignKey(PCR_target)

    def __str__(self):
        return self.sample.name+" has "+self.target.name


class lookup_table(models.Model):
    species = models.ForeignKey(Species)
    positive = models.ForeignKey(PCR_target)

    def __str__(self):
        return self.species.name


class Sample_reads(models.Model):
    sample = models.ForeignKey(Sample)
    reads = models.IntegerField()

    def __str__(self):
        return self.sample.name + " has " + str(self.reads) + "reads"